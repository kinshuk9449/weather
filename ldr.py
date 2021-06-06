from gpiozero import MCP3008
import time
import requests


adc = MCP3008(channel=1)

def getlight():
    return adc.value




        
