"""Isolated original-MTL loader candidate. Importing this file loads no models."""
from __future__ import annotations

import gc
import hashlib
import json
from pathlib import Path
import time


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def load_original_mtl_candidate(checkpoint_dir, evidence_dir):
    """Same CPU constructors/order/dtypes; mapped checkpoint storage is assigned."""
    import torch
    from safetensors.torch import load_file
    from chatterbox.mtl_tts import (ChatterboxMultilingualTTS, Conditionals,
                                   VoiceEncoder, T3, T3Config, S3Gen, MTLTokenizer)

    checkpoint_dir, evidence_dir = Path(checkpoint_dir), Path(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    report = {'candidate': 'original-mtl-cpu-assign-mmap', 'torchVersion': torch.__version__,
              'metaConstruction': False, 'dtypeConversion': False, 'components': [], 'rng': []}

    def save():
        (evidence_dir/'loader-verification.json').write_text(json.dumps(report, indent=2), encoding='utf8')

    def rng(label):
        raw = torch.get_rng_state().numpy().tobytes()
        target = evidence_dir/('rng-'+label+'.bin')
        target.write_bytes(raw)
        value = {'stage': label, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'file': target.name}
        report['rng'].append(value)
        save()
        return value['sha256']

    def tensor_hash(tensor):
        if tensor.device.type != 'cpu' or tensor.is_meta:
            raise RuntimeError('The candidate contains a non-CPU or meta tensor.')
        digest = hashlib.sha256()
        def add(value):
            if value.is_contiguous():
                flat = value.detach().reshape(-1)
                for start in range(0, flat.numel(), 262144):
                    # At most1MiB for F32,2MiB for I64; no full tensor clone.
                    digest.update(flat[start:start+262144].numpy().tobytes())
            elif value.ndim:
                for part in value: add(part)
            else:
                digest.update(value.detach().numpy().tobytes())
        add(tensor)
        return digest.hexdigest()

    def schema(tensor):
        return {'shape': list(tensor.shape), 'dtype': str(tensor.dtype),
                'stride': list(tensor.stride()), 'layout': str(tensor.layout)}

    def aliases(items):
        groups = {}
        for key, tensor in items:
            if tensor.numel():
                groups.setdefault((tensor.untyped_storage().data_ptr(), tensor.storage_offset()), []).append(key)
        return sorted(sorted(keys) for keys in groups.values() if len(keys) > 1)

    def auxiliary_tensors(module):
        result = {}
        for module_name, child in module.named_modules():
            for name in child._non_persistent_buffers_set:
                value = child._buffers.get(name)
                if torch.is_tensor(value):
                    result[module_name+'.buffer.'+name] = {**schema(value), 'sha256': tensor_hash(value)}
            for name, value in vars(child).items():
                if torch.is_tensor(value) and name not in child._parameters and name not in child._buffers:
                    result[module_name+'.attribute.'+name] = {**schema(value), 'sha256': tensor_hash(value)}
        return result

    def assign(module, state, label, expected, prior_aliases, auxiliaries):
        started = time.monotonic()
        if set(expected) != set(state):
            raise RuntimeError(label+' checkpoint keys differ from the original constructor.')
        component = {'name': label, 'keys': len(state), 'tensors': {}, 'strict': True}
        before = rng(label+'-before-assign')
        for key, value in state.items():
            if schema(value) != expected[key] or value.device.type != 'cpu':
                raise RuntimeError(label+' checkpoint tensor properties differ: '+key)
            component['tensors'][key] = dict(expected[key])
        module.load_state_dict(state, strict=True, assign=True)
        actual = module.state_dict()
        for key, value in actual.items():
            source = state[key]
            # Touch mapped weights only after old initialized parameters are released.
            component['tensors'][key]['checkpointValueSha256'] = tensor_hash(source)
            if schema(value) != expected[key] or tensor_hash(value) != component['tensors'][key]['checkpointValueSha256']:
                raise RuntimeError(label+' assigned tensor differs from its source: '+key)
            if value.numel() and (value.untyped_storage().data_ptr(), value.storage_offset()) != (source.untyped_storage().data_ptr(), source.storage_offset()):
                raise RuntimeError(label+' tensor assignment unexpectedly copied storage: '+key)
        after_aliases = aliases(module.named_parameters(remove_duplicate=False))
        if after_aliases != prior_aliases:
            raise RuntimeError(label+' parameter sharing differs from its constructor.')
        if auxiliary_tensors(module) != auxiliaries:
            raise RuntimeError(label+' auxiliary tensor changed during checkpoint assignment.')
        for child in module.modules():
            if isinstance(child, torch.nn.RNNBase):
                if any(value is not getattr(child, name) for name, value in zip(child._flat_weights_names, child._flat_weights)):
                    raise RuntimeError(label+' recurrent flat weights were not rebound.')
        if rng(label+'-after-assign') != before:
            raise RuntimeError(label+' checkpoint verification/assignment changed RNG state.')
        component.update(verified=True, checkpointStorageAssigned=True, aliases=after_aliases,
                         auxiliaryTensors=auxiliaries, verificationSeconds=round(time.monotonic()-started, 3))
        report['components'].append(component)
        save()

    def prepare(module, label):
        rng(label+'-after-constructor')
        # Keep only small metadata, not references to initialized parameter storage.
        expected = {key: schema(value) for key, value in module.state_dict().items()}
        return expected, aliases(module.named_parameters(remove_duplicate=False)), auxiliary_tensors(module)

    def load_state(path, label, safetensors=False):
        before = rng(label+'-before-checkpoint')
        state = load_file(str(path), device='cpu') if safetensors else torch.load(
            path, map_location=torch.device('cpu'), weights_only=True, mmap=True)
        if rng(label+'-after-checkpoint') != before:
            raise RuntimeError(label+' checkpoint loading changed RNG state.')
        return state

    rng('loader-entry')
    # Preserve the installed from_local constructor order exactly.
    ve = VoiceEncoder()
    expected, sharing, auxiliary = prepare(ve, 've')
    state = load_state(checkpoint_dir/'ve.pt', 've')
    assign(ve, state, 've', expected, sharing, auxiliary)
    del state, expected, sharing, auxiliary
    gc.collect()
    ve.to('cpu').eval()

    t3 = T3(T3Config.multilingual())
    expected, sharing, auxiliary = prepare(t3, 't3')
    state = load_state(checkpoint_dir/'t3_mtl23ls_v2.safetensors', 't3', safetensors=True)
    if 'model' in state:
        state = state['model'][0]
    assign(t3, state, 't3', expected, sharing, auxiliary)
    del state, expected, sharing, auxiliary
    gc.collect()
    t3.to('cpu').eval()

    s3gen = S3Gen()
    expected, sharing, auxiliary = prepare(s3gen, 's3gen')
    state = load_state(checkpoint_dir/'s3gen.pt', 's3gen')
    assign(s3gen, state, 's3gen', expected, sharing, auxiliary)
    del state, expected, sharing, auxiliary
    gc.collect()
    s3gen.to('cpu').eval()

    tokenizer = MTLTokenizer(str(checkpoint_dir/'grapheme_mtl_merged_expanded_v1.json'))
    conds = None
    if (checkpoint_dir/'conds.pt').exists():
        conds = Conditionals.load(checkpoint_dir/'conds.pt', map_location=torch.device('cpu')).to('cpu')
    rng('before-class-watermarker')
    model = ChatterboxMultilingualTTS(t3, s3gen, ve, tokenizer, 'cpu', conds=conds)
    rng('loader-exit')
    report['complete'] = True
    save()
    return model, report
