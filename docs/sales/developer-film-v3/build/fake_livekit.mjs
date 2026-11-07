// A stand-in for livekit-client, used ONLY in the film's capture browser (capture_room.py serves it in place of the CDN
// file). It connects to nothing: the demo participants are listed without cameras (tiles show their initials), and
// window.__filmSpeak(id) marks who is speaking. No network, no media.
export const RoomEvent = { ParticipantConnected: 'pc', ParticipantDisconnected: 'pd', TrackSubscribed: 'ts', TrackUnsubscribed: 'tu',
  LocalTrackPublished: 'lp', LocalTrackUnpublished: 'lu', TrackMuted: 'tm', TrackUnmuted: 'tn', ActiveSpeakersChanged: 'as',
  DataReceived: 'dr', Reconnecting: 'rc', AudioPlaybackStatusChanged: 'ap', Disconnected: 'dc' };
const PEOPLE = window.__filmPeople || [];
export class Room {
  constructor() {
    this.h = {}; this.canPlaybackAudio = true;
    this.localParticipant = { identity: 'me234567', name: 'Pierre', isMicrophoneEnabled: true, isCameraEnabled: false,
      setMicrophoneEnabled: async (v) => { this.localParticipant.isMicrophoneEnabled = v; }, setCameraEnabled: async (v) => { this.localParticipant.isCameraEnabled = false; },
      publishData: () => {} };
    this.remoteParticipants = new Map(PEOPLE.filter((p) => p.pid !== 'me234567').map((p) => [p.pid,
      { identity: p.pid, name: p.name, metadata: JSON.stringify({ role: p.role }), isMicrophoneEnabled: p.mic !== false }]));
    window.__filmRoom = this;
    window.__filmSpeak = (ids) => this.emit(RoomEvent.ActiveSpeakersChanged, ids.map((id) => ({ identity: id })));
  }
  on(e, f) { (this.h[e] = this.h[e] || []).push(f); return this; }
  emit(e, ...a) { (this.h[e] || []).forEach((f) => f(...a)); }
  async connect() { setTimeout(() => this.emit(RoomEvent.ParticipantConnected, { identity: 'x' }), 50); }
  async startAudio() {}
  async disconnect() {}
}
