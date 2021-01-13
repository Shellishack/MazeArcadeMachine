import RPi.GPIO as GPIO
import time


def shiftOut(data,clock,bin_val1,bin_val2):
    bin_val=bin_val1<<8;
    bin_val+=bin_val2;
    for x in range(16):
        GPIO.output(data,bin_val&0b1000000000000000)
        bin_val=bin_val<<1;
        
        GPIO.output(clock,1)
        GPIO.output(clock,0)

def toTwoBytes(bin_val1,bin_val2):
    bin_val=bin_val1<<8;
    bin_val+=bin_val2;
    return bin_val
        
def shiftOut_buff(data,clock,bin_val):
    for x in range(16):
        GPIO.output(data,bin_val&0b1000000000000000)
        bin_val=bin_val<<1;
        
        GPIO.output(clock,1)
        GPIO.output(clock,0)
    

