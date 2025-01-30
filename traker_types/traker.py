import sys
import os
import cv2
import argparse

class Traker:
  
  def __init__(self, traker_type):
    self.traker = self.get_traker(traker_type)
  
  def get_traker(self, traker_type):
    if traker_type == "BOOSTING":
      traker = cv2.legacy.TrackerBoosting_create()
    elif traker_type == "MIL":
      traker = cv2.legacy.TrackerMIL_create()
    elif traker_type == "KCF":
      traker = cv2.TrackerKCF_create()
    elif traker_type == "TLD":
      traker = cv2.TrackerTLD_create()
    elif traker_type == "MEDIANFLOW":
      traker = cv2.TrackerMedianFlow_create()
    elif traker_type == "MOSSE":
      traker = cv2.TrackerMOSSE_create()
    elif traker_type == "CSRT":
      traker = cv2.TrackerCSRT_create() 
    return traker

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Rastreamento de objetos')
  parser.add_argument('--traker_type', help='Tipo de rastreador')
  parser.add_argument('--video', help='Caminho do vídeo')
  args = parser.parse_args()
  
  traker = Traker(args.traker_type)
  print(f"Traker: {traker.traker}")