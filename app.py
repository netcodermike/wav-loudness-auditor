import wave,struct,math,json,argparse,unittest,tempfile
from pathlib import Path
def audit(path):
 with wave.open(str(path),'rb')as w:
  channels,width,rate,frames=w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes()
  if width!=2 or w.getcomptype()!='NONE':raise ValueError('Only uncompressed PCM16 WAV is supported')
  if frames==0:raise ValueError('WAV has no frames')
  data=w.readframes(frames)
  if len(data)!=frames*channels*2:raise ValueError('Truncated WAV payload')
  samples=struct.unpack('<'+'h'*(len(data)//2),data);report=[]
  for channel in range(channels):
   values=samples[channel::channels];peak=max(abs(x)for x in values)/32768;rms=math.sqrt(sum(x*x for x in values)/len(values))/32768;dc=sum(values)/len(values)/32768
   report.append(dict(channel=channel+1,peak_dbfs=20*math.log10(peak)if peak else None,rms_dbfs=20*math.log10(rms)if rms else None,dc_offset=dc,clipped_samples=sum(abs(x)>=32767 for x in values),crest_db=20*math.log10(peak/rms)if rms else None))
  return dict(file=str(path),sample_rate=rate,channels=channels,duration_seconds=frames/rate,measurements=report)
class Tests(unittest.TestCase):
 def test_known_signal_and_empty(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'x.wav'
   with wave.open(str(p),'wb')as w:w.setparams((1,2,8000,0,'NONE',''));w.writeframes(struct.pack('<hhhh',0,16384,0,-16384))
   r=audit(p);self.assertAlmostEqual(r['measurements'][0]['peak_dbfs'],-6.0206,places=3);self.assertEqual(r['measurements'][0]['dc_offset'],0)
   with wave.open(str(p),'wb')as w:w.setparams((1,2,8000,0,'NONE',''))
   with self.assertRaises(ValueError):audit(p)
if __name__=='__main__':
 p=argparse.ArgumentParser(description='PCM16 WAV RMS/peak audit; not LUFS or true-peak measurement');p.add_argument('file',nargs='?');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:unittest.main(argv=['audit'])
 elif a.file:print(json.dumps(audit(a.file),indent=2))
 else:p.error('file is required')
