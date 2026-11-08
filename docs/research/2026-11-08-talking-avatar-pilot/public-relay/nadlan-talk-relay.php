<?php
/** NadLan one-page conversation relay. Disabled until explicitly enabled. PHP 7.4+. */
if (!defined('ABSPATH')) { exit; }
if (!class_exists('nadlan_Talk_Relay')) {
final class nadlan_Talk_Relay {
    const NS = 'nadlan-talk/v1';
    const PAGE = '/en/buy-property-in-israel/';
    const COOKIE = 'nadlan_talk_session';
    const TTL = 900;
    const DEADLINE = 600;
    const LEASE = 45;
    const INPUT_LIMIT = 15728640;
    const OUTPUT_LIMIT = 4194304;
    const STORAGE_LIMIT = 134217728;
    const QUEUED = 4;

    public static function register() {
        foreach (array(
            array('/session', 'GET', 'session_route', 'visitor_read'),
            array('/health', 'GET', 'health', 'visitor_read'),
            array('/converse', 'POST', 'submit', 'visitor_write'),
            array('/requests/(?P<token>[A-Za-z0-9_-]{16,80})/cancel', 'POST', 'cancel', 'visitor_write'),
            array('/jobs/(?P<id>[a-f0-9]{32})', 'GET', 'status', 'visitor_owned'),
            array('/jobs/(?P<id>[a-f0-9]{32})/cancel', 'POST', 'cancel', 'visitor_write'),
            array('/audio/(?P<id>[a-f0-9]{32})/(?P<index>full|[0-7])', 'GET', 'audio', 'visitor_owned'),
            array('/worker/claim', 'POST', 'claim', 'worker_auth'),
            array('/worker/jobs/(?P<id>[a-f0-9]{32})', 'GET', 'worker_status', 'worker_auth'),
            array('/worker/jobs/(?P<id>[a-f0-9]{32})/update', 'POST', 'update', 'worker_auth')
        ) as $route) {
            register_rest_route(self::NS, $route[0], array('methods'=>$route[1], 'callback'=>array(__CLASS__,$route[2]), 'permission_callback'=>array(__CLASS__,$route[3])));
        }
    }
    private static function error($code, $message, $status=400) { return new WP_Error($code, $message, array('status'=>$status)); }
    private static function response($data, $status=200) {
        return new WP_REST_Response($data,$status,array('Cache-Control'=>'private, no-store, max-age=0','X-Content-Type-Options'=>'nosniff'));
    }
    public static function private_headers($result,$server,$request) {
        if(strpos($request->get_route(),'/'.self::NS.'/')===0 && $result instanceof WP_REST_Response){
            $result->header('Cache-Control','private, no-store, max-age=0');$result->header('X-Content-Type-Options','nosniff');
        }
        return $result;
    }
    private static function enabled() { return (bool)get_option('nadlan_talk_enabled',false); }
    private static function origin() {
        $url=wp_parse_url(home_url('/'));
        return $url['scheme'].'://'.$url['host'].(isset($url['port'])?':'.$url['port']:'');
    }
    public static function visitor_read($request) {
        $origin=$request->get_header('origin');
        if ($origin && $origin!==self::origin()) { return self::error('origin','This request is not allowed.',403); }
        if ($request->get_header('sec-fetch-site')==='cross-site') { return self::error('origin','This request is not allowed.',403); }
        $referer=wp_parse_url($request->get_header('referer'));
        if (!$referer || !isset($referer['host']) || $referer['host']!==wp_parse_url(home_url('/'),PHP_URL_HOST)
            || ($referer['path']??'')!==self::PAGE
            || ($referer['scheme'].'://'.$referer['host'].(isset($referer['port'])?':'.$referer['port']:''))!==self::origin()) {
            return self::error('page','Please open the conversation on the English buying guide.',403);
        }
        return true;
    }
    private static function session_value() {
        $value=isset($_COOKIE[self::COOKIE])?(string)$_COOKIE[self::COOKIE]:'';
        if (!preg_match('/^([a-f0-9]{32})\.([0-9]{10})\.([a-f0-9]{64})$/',$value,$m) || (int)$m[2]<time()) { return null; }
        return hash_equals(hash_hmac('sha256',$m[1].'.'.$m[2],wp_salt('auth')),$m[3]) ? $m[1] : null;
    }
    private static function owner() { $id=self::session_value(); return $id?hash_hmac('sha256',$id,wp_salt('secure_auth')):null; }
    private static function csrf($id,$day=null) { return hash_hmac('sha256','talk|'.$id.'|'.($day===null?gmdate('Ymd'):$day),wp_salt('nonce')); }
    public static function visitor_owned($request) {
        $allowed=self::visitor_read($request);
        return is_wp_error($allowed)?$allowed:(self::owner()?true:self::error('session_required','Please reopen the conversation.',409));
    }
    public static function visitor_write($request) {
        $allowed=self::visitor_owned($request); if (is_wp_error($allowed)) { return $allowed; }
        if ($request->get_header('origin')!==self::origin()) { return self::error('origin','This request is not allowed.',403); }
        $id=self::session_value(); $token=(string)$request->get_header('x-nl-csrf');
        return hash_equals(self::csrf($id),$token)||hash_equals(self::csrf($id,gmdate('Ymd',time()-86400)),$token)
            ?true:self::error('csrf','Please reopen the conversation.',403);
    }
    public static function worker_auth($request) {
        // WordPress validates the existing application password. Never accept a visitor nonce here.
        $uuid=function_exists('rest_get_authenticated_app_password')?rest_get_authenticated_app_password():null;
        return current_user_can('manage_options') && $uuid ? true : self::error('worker_auth','Authentication required.',401);
    }
    private static function lock() {
        global $wpdb;
        $value=time().'|'.bin2hex(random_bytes(12));
        for($attempt=0;$attempt<5;$attempt++) {
            if (add_option('nadlan_talk_lock',$value,'',false)) { return $value; }
            $old=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",'nadlan_talk_lock'));
            if ($old && (int)$old<time()-30) {
                $wpdb->query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",'nadlan_talk_lock',$old));
                wp_cache_delete('nadlan_talk_lock','options');
            }
            usleep(10000);
        }
        return null;
    }
    private static function unlock($value) {
        global $wpdb;
        $wpdb->query($wpdb->prepare("DELETE FROM {$wpdb->options} WHERE option_name=%s AND option_value=%s",'nadlan_talk_lock',$value));
        wp_cache_delete('nadlan_talk_lock','options');
    }
    private static function locked($callback) {
        $lock=self::lock(); if (!$lock) { return self::error('busy','Please try again shortly.',429); }
        try { self::cleanup(); return $callback(); } finally { self::unlock($lock); }
    }
    private static function get_job($id) { return get_transient('nadlan_talk_j_'.$id); }
    private static function save_job($job) { set_transient('nadlan_talk_j_'.$job['id'],$job,max(1,$job['expiresAt']-time())); }
    private static function blob_key($id,$index) { return 'nadlan_talk_b_'.$id.'_'.$index; }
    private static function save_blob($id,$index,$bytes,$ttl) { return set_transient(self::blob_key($id,$index),base64_encode($bytes),$ttl); }
    private static function load_blob($id,$index) { $encoded=get_transient(self::blob_key($id,$index));return is_string($encoded)?base64_decode($encoded,true):false; }
    private static function purge_blobs($job) {
        foreach(array_merge(array('input','full'),range(0,7)) as $index) { delete_transient(self::blob_key($job['id'],$index)); }
    }
    private static function terminal($job) { return in_array($job['phase'],array('done','error','cancelled'),true); }
    private static function stop_job(&$job,$phase='cancelled',$message='The reply was cancelled.') {
        $job['phase']=$phase; $job['error']=$message; $job['chunks']=array(); unset($job['result']);
        $job['storedBytes']=0;
        self::purge_blobs($job); self::save_job($job);
    }
    private static function cleanup() {
        $ids=get_option('nadlan_talk_jobs',array()); $kept=array();
        foreach(is_array($ids)?$ids:array() as $id) {
            $job=self::get_job($id);
            if (!$job || $job['expiresAt']<=time()) {
                self::purge_blobs(array('id'=>$id));delete_transient('nadlan_talk_j_'.$id);continue;
            }
            if (!self::terminal($job) && ($job['deadlineAt']<=time() || (!empty($job['leaseUntil']) && $job['leaseUntil']<=time()))) {
                self::stop_job($job,'error','The reply could not finish. Please ask again.');
            }
            $kept[]=$id;
        }
        if ($kept!==$ids) { update_option('nadlan_talk_jobs',$kept,false); }
    }
    private static function rate($key,$limit,$seconds) {
        $key='nadlan_talk_r_'.hash('sha256',$key);$count=(int)get_transient($key);
        if($count>=$limit){return false;} set_transient($key,$count+1,$seconds);return true;
    }
    private static function ip_key() { return hash_hmac('sha256',$_SERVER['REMOTE_ADDR']??'unknown',wp_salt('auth')); }
    private static function storage_bytes() {
        $total=0;foreach(get_option('nadlan_talk_jobs',array()) as $id){$job=self::get_job($id);if($job){$total+=(int)($job['storedBytes']??0);}}return $total;
    }
    private static function request_key($owner,$token) { return 'nadlan_talk_t_'.hash('sha256',$owner.'|'.$token); }
    private static function available() { $worker=get_transient('nadlan_talk_worker');return self::enabled() && $worker && !empty($worker['ready']) && $worker['seenAt']>=time()-30; }
    public static function health($request) { $worker=get_transient('nadlan_talk_worker');return self::response(array('available'=>(bool)self::available(),'unavailableCode'=>self::available()?null:($worker['unavailableCode']??'local_unavailable'))); }
    public static function session_route($request) {
        return self::locked(function(){
            if(!self::rate('session:'.self::ip_key(),60,600)){return self::error('rate','Please try again shortly.',429);}
            $id=self::session_value();
            if(!$id){$id=bin2hex(random_bytes(16));$expiry=time()+3600;$raw=$id.'.'.$expiry;
                setcookie(self::COOKIE,$raw.'.'.hash_hmac('sha256',$raw,wp_salt('auth')),array('expires'=>$expiry,'path'=>'/','secure'=>is_ssl(),'httponly'=>true,'samesite'=>'Strict'));
            }
            return self::response(array('ready'=>true,'available'=>(bool)self::available(),'csrf'=>self::csrf($id),'maxRecordingSeconds'=>20,'maxUploadBytes'=>self::INPUT_LIMIT,'pollInterval'=>1000));
        });
    }
    private static function public_job($job) {
        $data=array('jobId'=>$job['id'],'requestId'=>$job['requestId'],'phase'=>$job['phase'],'expiresAt'=>$job['expiresAt'],'deadlineAt'=>$job['deadlineAt'],
            'jobUrl'=>rest_url(self::NS.'/jobs/'.$job['id']),'userText'=>$job['userText']??$job['text'],'responseText'=>$job['responseText']??'','chunks'=>$job['chunks']);
        if(isset($job['result'])){$data['result']=$job['result'];}
        if(isset($job['error'])){$data['error']=$job['error'];}
        if(isset($job['errorCode'])){$data['errorCode']=$job['errorCode'];}
        return $data;
    }
    public static function submit($request) {
        $owner=self::owner();$token=(string)$request->get_header('x-nl-request-id');
        if(!preg_match('/^[A-Za-z0-9_-]{16,80}$/',$token)){return self::error('request_id','Please resend the question.',400);}
        $size=(int)($_SERVER['CONTENT_LENGTH']??0);if($size<=0 || $size>self::INPUT_LIMIT){return self::error('upload_size','Please send a shorter recording.',413);}
        $text='';$audio=null;$mime=null;$duration=0;
        $files=$request->get_file_params();
        if(isset($files['audio'])){
            $file=$files['audio'];$duration=(float)$request->get_param('duration');
            if($file['error']!==UPLOAD_ERR_OK || $duration<=0 || $duration>20 || !is_uploaded_file($file['tmp_name']) || $file['size']>self::INPUT_LIMIT){return self::error('audio','Please record a question of twenty seconds or less.',400);}
            $mime=explode(';',(string)$file['type'])[0];
            if(!in_array($mime,array('audio/webm','audio/mp4','audio/ogg','audio/wav','audio/x-wav'),true)){return self::error('audio','That recording format is not supported.',415);}
            $audio=file_get_contents($file['tmp_name']);if(!$audio){return self::error('audio','The recording was empty.',400);}
        }else{
            $body=$request->get_json_params();$text=isset($body['text'])&&is_string($body['text'])?trim($body['text']):'';
            if(!$text || mb_strlen($text)>1200){return self::error('text','Please type one short question.',400);}
        }
        return self::locked(function()use($owner,$token,$text,$audio,$mime,$duration){
            $key=self::request_key($owner,$token);$prior=get_transient($key);
            if($prior && !empty($prior['cancelled'])){return self::response(array('phase'=>'cancelled','requestId'=>$token),409);}
            if($prior && !empty($prior['jobId'])){$job=self::get_job($prior['jobId']);if($job){return self::response(self::public_job($job),202);}}
            if(!self::available()){return self::error('unavailable','Voice conversation is unavailable just now. Please try again shortly.',503);}
            $ids=get_option('nadlan_talk_jobs',array());$pending=0;
            foreach($ids as $id){$old=self::get_job($id);if($old && !self::terminal($old)){
                if($old['owner']===$owner){self::stop_job($old);}else{$pending++;}
            }}
            if($pending>=self::QUEUED+1 || count($ids)>=128){return self::error('busy','The voice is busy. Please try again shortly.',429);}
            if(self::storage_bytes()+strlen($audio??'')>self::STORAGE_LIMIT){return self::error('busy','The voice is busy. Please try again shortly.',429);}
            if(!self::rate('start:'.$owner,6,600) || !self::rate('start-ip:'.self::ip_key(),20,3600) || !self::rate('start-global',60,3600)){return self::error('rate','Please try again shortly.',429);}
            $id=bin2hex(random_bytes(16));$job=array('id'=>$id,'owner'=>$owner,'requestId'=>$token,'text'=>$text,'phase'=>'queued','createdAt'=>time(),'expiresAt'=>time()+self::TTL,'deadlineAt'=>time()+self::DEADLINE,'chunks'=>array(),'inputMime'=>$mime,'durationHint'=>$duration,'storedBytes'=>strlen($audio??''),'inputBytes'=>strlen($audio??''));
            if($audio!==null && !self::save_blob($id,'input',$audio,self::TTL)){return self::error('storage','The recording could not be saved. Please try again.',503);}
            self::save_job($job);$ids[]=$id;update_option('nadlan_talk_jobs',$ids,false);set_transient($key,array('jobId'=>$id),self::TTL);
            return self::response(self::public_job($job),202);
        });
    }
    public static function cancel($request) {
        return self::locked(function()use($request){
            $owner=self::owner();$id=$request->get_param('id');$token=$request->get_param('token');
            if(!self::rate('cancel:'.self::ip_key(),120,600)){return self::error('rate','Please try again shortly.',429);}
            if($id){$job=self::get_job($id);if(!$job||$job['owner']!==$owner){return self::error('not_found','Question not found.',404);}$token=$job['requestId'];}
            $key=self::request_key($owner,$token);$prior=get_transient($key);
            set_transient($key,array('cancelled'=>true,'jobId'=>$prior['jobId']??$id),self::TTL);
            $id=$id?:($prior['jobId']??null);$job=$id?self::get_job($id):null;
            if($job && $job['owner']===$owner){self::stop_job($job);}
            return self::response(array('phase'=>'cancelled','requestId'=>$token));
        });
    }
    public static function status($request) {
        return self::locked(function()use($request){$job=self::get_job($request['id']);return $job&&$job['owner']===self::owner()?self::response(self::public_job($job)):self::error('not_found','Question not found.',404);});
    }
    public static function audio($request) {
        $job=self::get_job($request['id']);$index=$request['index'];
        if(!$job||$job['owner']!==self::owner()||in_array($job['phase'],array('error','cancelled'),true)||$job['expiresAt']<=time()
            || (!self::terminal($job)&&($job['deadlineAt']<=time()||(!empty($job['leaseUntil'])&&$job['leaseUntil']<=time())))) {return self::error('not_found','Audio not found.',404);}
        $bytes=self::load_blob($job['id'],$index);
        return $bytes!==false?self::response(array('_nadlan_audio'=>$bytes)):self::error('not_found','Audio not found.',404);
    }
    public static function serve_audio($served,$result,$request,$server) {
        if(strpos($request->get_route(),'/'.self::NS.'/audio/')!==0 || !($result instanceof WP_REST_Response)){return $served;}
        $data=$result->get_data();if(!is_array($data)||!isset($data['_nadlan_audio'])){return $served;}
        header('Content-Type: audio/wav');header('Cache-Control: private, no-store, max-age=0');header('X-Content-Type-Options: nosniff');header('Content-Length: '.strlen($data['_nadlan_audio']));if($request->get_method()!=='HEAD'){echo $data['_nadlan_audio'];}return true;
    }
    private static function worker_state($request) {
        $body=$request->get_json_params();$worker=isset($body['workerId'])?(string)$body['workerId']:'';
        if(!preg_match('/^[A-Za-z0-9_-]{8,64}$/',$worker)){return null;}
        $code=($body['unavailableCode']??'')==='resource_busy'?'resource_busy':'local_unavailable';
        set_transient('nadlan_talk_worker',array('workerId'=>$worker,'ready'=>!empty($body['ready']),'unavailableCode'=>$code,'seenAt'=>time()),35);return $worker;
    }
    public static function claim($request) {
        return self::locked(function()use($request){
            $worker=self::worker_state($request);if(!$worker){return self::error('worker_id','Invalid worker identifier.',400);}
            if(!self::available()){return self::response(array('job'=>null,'enabled'=>self::enabled()));}
            $jobs=array();foreach(get_option('nadlan_talk_jobs',array()) as $id){$job=self::get_job($id);if($job&&!self::terminal($job)){$jobs[]=$job;if(!empty($job['leaseToken'])){return self::response(array('job'=>null));}}}
            if(!$jobs){return self::response(array('job'=>null));}$job=$jobs[0];
            $job['leaseToken']=bin2hex(random_bytes(24));$job['workerId']=$worker;$job['leaseUntil']=time()+self::LEASE;$job['phase']='claimed';self::save_job($job);
            $data=array('jobId'=>$job['id'],'leaseToken'=>$job['leaseToken'],'ownerKey'=>$job['owner'],'requestId'=>$job['requestId'],'text'=>$job['text'],'mime'=>$job['inputMime'],'durationHint'=>$job['durationHint'],'deadlineAt'=>$job['deadlineAt'],'expiresAt'=>$job['expiresAt'],'leaseUntil'=>$job['leaseUntil'],'cancelled'=>false,'maxRecordingSeconds'=>20);
            if($job['inputMime']){$bytes=self::load_blob($job['id'],'input');if($bytes===false){self::stop_job($job,'error','The recording expired. Please try again.');return self::error('input_expired','The recording expired.',410);}$data['audioBase64']=base64_encode($bytes);}
            return self::response(array('job'=>$data));
        });
    }
    private static function leased_job($request) {
        $job=self::get_job($request['id']);$body=$request->get_json_params();$token=$request->get_header('x-nl-lease')?:($body['leaseToken']??'');
        if(!$job||empty($job['leaseToken'])||!hash_equals($job['leaseToken'],(string)$token)){return self::error('lease','Lease not found.',404);}return $job;
    }
    public static function worker_status($request) {
        return self::locked(function()use($request){$job=self::leased_job($request);if(is_wp_error($job)){return $job;}return self::response(array('cancelled'=>self::terminal($job)&&$job['phase']!=='done','phase'=>$job['phase'],'deadlineAt'=>$job['deadlineAt'],'leaseUntil'=>$job['leaseUntil']));});
    }
    private static function decode_wav($body) {
        $base=$body['audioBase64']??'';if(!is_string($base)||strlen($base)>ceil(self::OUTPUT_LIMIT/3)*4){return null;}
        $bytes=base64_decode($base,true);
        return $bytes!==false && strlen($bytes)>=44 && strlen($bytes)<=self::OUTPUT_LIMIT && substr($bytes,0,4)==='RIFF' && substr($bytes,8,4)==='WAVE'?$bytes:null;
    }
    public static function update($request) {
        return self::locked(function()use($request){
            $job=self::leased_job($request);if(is_wp_error($job)){return $job;}
            if(self::terminal($job)){return self::response(array('accepted'=>false,'cancelled'=>$job['phase']!=='done','phase'=>$job['phase']),409);}
            $body=$request->get_json_params();$event=$body['event']??'';$job['leaseUntil']=min(time()+self::LEASE,$job['deadlineAt']);
            set_transient('nadlan_talk_worker',array('workerId'=>$job['workerId'],'ready'=>true,'seenAt'=>time()),35);
            if($event==='heartbeat'){}
            elseif($event==='progress'){
                $phase=$body['phase']??'';if(!in_array($phase,array('transcribing','thinking','synthesizing','streaming'),true)){return self::error('phase','Invalid phase.',400);}$job['phase']=$phase;
                foreach(array('userText','responseText') as $field){if(isset($body[$field])){$job[$field]=mb_substr(sanitize_text_field($body[$field]),0,2000);}}
                if(!empty($body['inputConsumed'])){delete_transient(self::blob_key($job['id'],'input'));$job['storedBytes']-=($job['inputBytes']??0);$job['inputBytes']=0;}
            }
            elseif($event==='chunk'||$event==='done'){
                $bytes=self::decode_wav($body);if($bytes===null){return self::error('audio','A valid bounded WAV is required.',400);}
                $text=isset($body['text'])&&is_string($body['text'])?sanitize_text_field($body['text']):'';
                if(!$text||mb_strlen($text)>2000){return self::error('text','Response text is required.',400);}
                $index=$event==='done'?'full':($body['index']??null);
                if($event==='chunk'&&(!is_int($index)||$index<0||$index>7||$index>count($job['chunks']))){return self::error('index','Sentence order is invalid.',409);}
                $hash=hash('sha256',$bytes.'|'.$text);
                if($event==='chunk'&&isset($job['chunks'][$index])){
                    if(($job['chunkHashes'][$index]??'')!==$hash){return self::error('changed','Published sentence cannot change.',409);}
                    self::save_job($job);return self::response(array('accepted'=>true,'duplicate'=>true,'cancelled'=>false));
                }
                $item=array('audioUrl'=>rest_url(self::NS.'/audio/'.$job['id'].'/'.$index),'text'=>$text,'cues'=>array(),'duration'=>max(0,min(180,(float)($body['duration']??0))));
                if(self::storage_bytes()+strlen($bytes)>self::STORAGE_LIMIT){return self::error('busy','The voice is busy. Please try again shortly.',429);}
                if(!self::save_blob($job['id'],$index,$bytes,max(1,$job['expiresAt']-time()))){return self::error('storage','The reply could not be saved.',503);}
                $job['storedBytes']+=strlen($bytes);
                if($event==='chunk'){$item['index']=$index;$job['chunks'][]=$item;$job['chunkHashes'][]=$hash;$job['phase']='streaming';}
                else{$job['result']=$item;$job['result']['voiceEngine']=sanitize_key($body['voiceEngine']??'');$job['result']['voiceCacheHit']=!empty($body['voiceCacheHit']);$job['phase']='done';$job['responseText']=$text;if(isset($body['userText'])){$job['userText']=mb_substr(sanitize_text_field($body['userText']),0,2000);}delete_transient(self::blob_key($job['id'],'input'));$job['storedBytes']-=($job['inputBytes']??0);$job['inputBytes']=0;}
            }
            elseif($event==='error'){
                $code=$body['errorCode']??'failed';$job['errorCode']=$code==='resource_busy'?'resource_busy':'failed';
                self::stop_job($job,'error',$code==='resource_busy'?'This computer is busy. Please try again shortly.':'The reply could not finish. Please ask again.');
            }else{return self::error('event','Invalid event.',400);}
            self::save_job($job);return self::response(array('accepted'=>true,'cancelled'=>false,'phase'=>$job['phase'],'leaseUntil'=>$job['leaseUntil'],'deadlineAt'=>$job['deadlineAt']));
        });
    }
}
add_action('rest_api_init',array('nadlan_Talk_Relay','register'));
add_filter('rest_post_dispatch',array('nadlan_Talk_Relay','private_headers'),10,3);
add_filter('rest_pre_serve_request',array('nadlan_Talk_Relay','serve_audio'),10,4);
}
