import cv2
import argparse
import sys

class Traker:
  
  def __init__(self, traker_type, video):
    self.traker = self.get_traker(traker_type)
    self.video = cv2.VideoCapture(video)
    if not self.video.isOpened():
      print('Não foi Qpossível carregar o vídeo')
      sys.exit()
  
  def get_traker(self, traker_type):
    if traker_type == "BOOSTING":
      traker = cv2.legacy.TrackerBoosting_create()
      print("[INFO] Rastreador BOOSTING selecionado")
    # elif traker_type == "MIL":
    #   traker = cv2.legacy.TrackerMIL_create()
    # elif traker_type == "KCF":
    #   traker = cv2.TrackerKCF_create()
    # elif traker_type == "TLD":
    #   traker = cv2.TrackerTLD_create()
    # elif traker_type == "MEDIANFLOW":
    #   traker = cv2.TrackerMedianFlow_create()
    # elif traker_type == "MOSSE":
    #   traker = cv2.TrackerMOSSE_create()
    # elif traker_type == "CSRT":
    #   traker = cv2.TrackerCSRT_create() 
    return traker

  def process_video(self,only_frame, start_roi=None, output=None, ):
    ok, frame = self.video.read()
    if not ok:
      print('[ERRO] Não foi possível ler o frame')
      sys.exit()
      
    bbox = start_roi
    ok = self.traker.init(frame, bbox)
      
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    if output is not None:
      out = cv2.VideoWriter(output, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
    else:
      out = cv2.VideoWriter('./output.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
    
    print('[INFO] Processando vídeo...')
    if not only_frame:
      while True:
        ok, frame = self.video.read()
        if not ok:
          break
        ok, bbox = self.traker.update(frame)
        if ok:
          (x, y, w, h) = [int(v) for v in bbox]
          cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
          break
        out.write(frame)
    else:
      ok, frame = self.video.read()
      ok, bbox = self.traker.update(frame)
      if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      out.write(frame)
    
    self.video.release()
    out.release()
    try:
      cv2.destroyAllWindows()
    except:
      pass
    print('[INFO] Vídeo processado com sucesso')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Rastreamento de objetos em vídeos')
  parser.add_argument('--traker_type', help='Tipo de rastreador', required=True, choices=['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT'])
  parser.add_argument('--video', help='Caminho do vídeo', required=True)
  parser.add_argument('--start_roi', help='Coordenadas iniciais da ROI (x y largura altura)', nargs=4, type=int, metavar=('X', 'Y', 'LARGURA', 'ALTURA'), required=True)
  parser.add_argument('--output', help='Caminho do vídeo de saída')
  parser.add_argument('--only-frame', help='Processar apenas um frame', const=True, action='store_const')
  args = parser.parse_args()
  
  traker = Traker(args.traker_type, args.video)
  traker.process_video(args.only_frame, args.start_roi, args.output,)