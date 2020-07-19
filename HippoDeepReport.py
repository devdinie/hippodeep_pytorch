#!/usr/local/fsl/fslpython/bin/python3
#
# requests a T1 NIFTI image that previousely was used for HippoDeep processing
# reads the Hippodeep output file *_mask_L.nii.gz, *_mask_R.nii.gz and *_hippoLR_volumes.csv
# and gebnerates a PDF report file
#
# ----- VERSION HISTORY -----
#
# Version 0.1 - 10, July 2020
#       - 1st public github Release
#
# ----- LICENSE -----                 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    For more detail see the GNU General Public License.
#    <http://www.gnu.org/licenses/>.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
# ----- REQUIREMENTS ----- 
#
#    This program was developed under Python Version 3.7
#    with the following additional libraries: 
#    - numpy
#    - nibabel
#    - pillow
#    - fpdf2 (aka PyFPDF)
#      also works with fpdf (versions<2) using temprary PDF files on disk
#
# OBS: For Output Language customization edit the first line in the .csv file
#

from __future__ import print_function
try: import win32gui, win32console
except: pass #silent
from math import floor
import sys
import os
import csv
from io import BytesIO
import numpy as np
import nibabel as nib
from GetFilename import GetFilename
from PIL import Image
from fpdf import FPDF
from fpdf import __version__ as fpdf_version



def HippoDeepReport(SpatResol, data0, data1, data2, data3, text0, text1, text2, text3, filename):
    
    #define some color lookup tables    
        
    lut_gray = np.zeros ([256,3], dtype=np.uint8)
    lut_gray  [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_gray  [:,1] = lut_gray  [:,0]
    lut_gray  [:,2] = lut_gray  [:,0]
    lut_gray = lut_gray.astype(np.uint8)

    lut_red  = np.zeros ([256,3], dtype=np.uint8)
    lut_red [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_red = lut_red.astype(np.uint8)

    lut_green = np.zeros ([256,3], dtype=np.uint8)
    lut_green[:,1] = np.linspace(0, 255, num=256, endpoint=True)
    lut_green = lut_green.astype(np.uint8)

    lut_blue = np.zeros ([256,3], dtype=np.uint8)
    lut_blue[:,2] = np.linspace(0, 255, num=256, endpoint=True)
    lut_blue = lut_blue.astype(np.uint8)

    lut_yellow  = np.zeros ([256,3], dtype=np.uint8)
    lut_yellow [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_yellow [:,1] = lut_yellow [:,0]
    lut_yellow = lut_yellow.astype(np.uint8)

    lut_magenta = np.zeros ([256,3], dtype=np.uint8)
    lut_magenta [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_magenta [:,2] = lut_magenta [:,0]
    lut_magenta = lut_magenta.astype(np.uint8)

    lut_cyan = np.zeros ([256,3], dtype=np.uint8)
    lut_cyan [:,1] = np.linspace(0, 255, num=256, endpoint=True)
    lut_cyan [:,2] = lut_cyan [:,1]
    lut_cyan = lut_cyan.astype(np.uint8)

    #http://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_B.html#sect_B.1.1
    lut_hotiron = np.asarray([
    [ 0, 0,0],[ 2, 0,0],[ 4, 0,0],[ 6, 0,0],[ 8, 0,0],[ 10,0,0],[ 12,0,0],[ 14,0,0],
    [ 16,0,0],[ 18,0,0],[ 20,0,0],[ 22,0,0],[ 24,0,0],[ 26,0,0],[ 28,0,0],[ 30,0,0],
    [ 32,0,0],[ 34,0,0],[ 36,0,0],[ 38,0,0],[ 40,0,0],[ 42,0,0],[ 44,0,0],[ 46,0,0],
    [ 48,0,0],[ 50,0,0],[ 52,0,0],[ 54,0,0],[ 56,0,0],[ 58,0,0],[ 60,0,0],[ 62,0,0],
    [ 64,0,0],[ 66,0,0],[ 68,0,0],[ 70,0,0],[ 72,0,0],[ 74,0,0],[ 76,0,0],[ 78,0,0],
    [ 80,0,0],[ 82,0,0],[ 84,0,0],[ 86,0,0],[ 88,0,0],[ 90,0,0],[ 92,0,0],[ 94,0,0],
    [ 96,0,0],[ 98,0,0],[100,0,0],[102,0,0],[104,0,0],[106,0,0],[108,0,0],[110,0,0],
    [112,0,0],[114,0,0],[116,0,0],[118,0,0],[120,0,0],[122,0,0],[124,0,0],[126,0,0],
    [128,0,0],[130,0,0],[132,0,0],[134,0,0],[136,0,0],[138,0,0],[140,0,0],[142,0,0],
    [144,0,0],[146,0,0],[148,0,0],[150,0,0],[152,0,0],[154,0,0],[156,0,0],[158,0,0],
    [160,0,0],[162,0,0],[164,0,0],[166,0,0],[168,0,0],[170,0,0],[172,0,0],[174,0,0],
    [176,0,0],[178,0,0],[180,0,0],[182,0,0],[184,0,0],[186,0,0],[188,0,0],[190,0,0],
    [192,0,0],[194,0,0],[196,0,0],[198,0,0],[200,0,0],[202,0,0],[204,0,0],[206,0,0],
    [208,0,0],[210,0,0],[212,0,0],[214,0,0],[216,0,0],[218,0,0],[220,0,0],[222,0,0],
    [224,0,0],[226,0,0],[228,0,0],[230,0,0],[232,0,0],[234,0,0],[236,0,0],[238,0,0],
    [240,0,0],[242,0,0],[244,0,0],[246,0,0],[248,0,0],[250,0,0],[252,0,0],[254,0,0],
    [255, 0, 0],[255, 2, 0],[255, 4, 0],[255, 6, 0],[255, 8, 0],[255, 10,0],[255, 12,0],[255, 14,0],
    [255, 16,0],[255, 18,0],[255, 20,0],[255, 22,0],[255, 24,0],[255, 26,0],[255, 28,0],[255, 30,0],
    [255, 32,0],[255, 34,0],[255, 36,0],[255, 38,0],[255, 40,0],[255, 42,0],[255, 44,0],[255, 46,0],
    [255, 48,0],[255, 50,0],[255, 52,0],[255, 54,0],[255, 56,0],[255, 58,0],[255, 60,0],[255, 62,0],
    [255, 64,0],[255, 66,0],[255, 68,0],[255, 70,0],[255, 72,0],[255, 74,0],[255, 76,0],[255, 78,0],
    [255, 80,0],[255, 82,0],[255, 84,0],[255, 86,0],[255, 88,0],[255, 90,0],[255, 92,0],[255, 94,0],
    [255, 96,0],[255, 98,0],[255,100,0],[255,102,0],[255,104,0],[255,106,0],[255,108,0],[255,110,0],
    [255,112,0],[255,114,0],[255,116,0],[255,118,0],[255,120,0],[255,122,0],[255,124,0],[255,126,0],
    [255,128,  4],[255,130,  8],[255,132, 12],[255,134, 16],[255,136, 20],[255,138, 24],[255,140, 28],[255,142, 32],
    [255,144, 36],[255,146, 40],[255,148, 44],[255,150, 48],[255,152, 52],[255,154, 56],[255,156, 60],[255,158, 64],
    [255,160, 68],[255,162, 72],[255,164, 76],[255,166, 80],[255,168, 84],[255,170, 88],[255,172, 92],[255,174, 96],
    [255,176,100],[255,178,104],[255,180,108],[255,182,112],[255,184,116],[255,186,120],[255,188,124],[255,190,128],
    [255,192,132],[255,194,136],[255,196,140],[255,198,144],[255,200,148],[255,202,152],[255,204,156],[255,206,160],
    [255,208,164],[255,210,168],[255,212,172],[255,214,176],[255,216,180],[255,218,184],[255,220,188],[255,222,192],
    [255,224,196],[255,226,200],[255,228,204],[255,230,208],[255,232,212],[255,234,216],[255,236,220],[255,238,224],
    [255,240,228],[255,242,232],[255,244,236],[255,246,240],[255,248,244],[255,250,248],[255,252,252],[255,255,255]])
    lut_hotiron = lut_hotiron.astype(np.uint8)

    lut_rediron = lut_hotiron # alias

    lut_greeniron  = np.zeros ([256,3], dtype=np.uint8)
    lut_greeniron [:,0] = lut_hotiron [:,2]    
    lut_greeniron [:,1] = lut_hotiron [:,0]  
    lut_greeniron [:,2] = lut_hotiron [:,1] 

    lut_blueiron  = np.zeros ([256,3], dtype=np.uint8)
    lut_blueiron [:,0] = lut_hotiron [:,2]    
    lut_blueiron [:,1] = lut_hotiron [:,1]  
    lut_blueiron [:,2] = lut_hotiron [:,0]  

    transparancy = 0.4 # 0.5 is half-transparent, 1.0 is not-transparent 
    lut_left = lut_green
    lut_right = lut_red

    #write PDF header
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 28, txt=text0, ln=1, align="C")
    pdf.set_font("Courier", 'B', size=12)
    pdf.cell(200, 5, txt=text1, ln=1, align="L")
    pdf.set_text_color(0, 140, 0)
    pdf.cell(200, 5, txt=text2, ln=1, align="L")
    pdf.set_text_color(170, 0, 0)
    pdf.cell(200, 5, txt=text3, ln=1, align="L")

    # image positioning
    xoffset=10
    yoffset=55
    #slice_per_line=6; width=30 # very small
    slice_per_line=5; width=38  # looks best
    #slice_per_line=4; width=47 # may no fit on a single page
    sparator=2
    
    # --------------------------------------- CROP in Y (AP) -----------------------------------------   
    
    # crop data in Y (otherwise may not fit on one page)
    data3_axis1 = np.sum(np.sum(data3, axis=0), axis=1)     
    min_axis1 = np.min(np.nonzero(data3_axis1))
    max_axis1 = np.max(np.nonzero(data3_axis1))
    delta=int(.2*(max_axis1-min_axis1))
    min_axis1 = max (0,min_axis1-delta)
    max_axis1 = min (data3.shape[1],max_axis1+delta)     
    data0 = data0 [:, min_axis1:max_axis1, :] 
    data1 = data1 [:, min_axis1:max_axis1, :]
    data2 = data2 [:, min_axis1:max_axis1, : ]
    data0 /= np.max(data0) 
    
    # --------------------------------------- CROP in Z (FH) -----------------------------------------   
     
    # crop data in Z (otherwise may not fit on one page)
    data3_axis2 = np.sum(np.sum(data3, axis=0), axis=0)     
    min_axis2 = np.min(np.nonzero(data3_axis2))
    max_axis2 = np.max(np.nonzero(data3_axis2))
    delta=int(.1*(max_axis2-min_axis2))
    min_axis2 = max (0,min_axis2-delta)
    max_axis2 = min (data3.shape[2],max_axis2+delta)     
    data0 = data0 [:, :, min_axis2:max_axis2] 
    data1 = data1 [:, :, min_axis2:max_axis2]
    data2 = data2 [:, :, min_axis2:max_axis2]
    data0 /= np.max(data0)    
    
    
    # --------------------------------------- AXIAL ----------------------------------------------

    # transformations
    data0 = np.rot90(data0, axes=(0,1))
    data1 = np.rot90(data1, axes=(0,1))
    data2 = np.rot90(data2, axes=(0,1))
    SpatResol[1], SpatResol[0] = SpatResol[0], SpatResol[1]

    # find all slices that contain some part of either ROI 
    slices=[]; npoints=[]
    thresh = int(0.001*data0.shape[0]*data0.shape[1])
    for slice in range (0,data0.shape[2]):
      nz1=np.nonzero(data1[:,:,slice])
      nz2=np.nonzero(data2[:,:,slice])
      if len(nz1[0])>thresh and len(nz2[0])>thresh: slices.append(slice); npoints.append(len(nz1[0]))
      
    # choose a subset of these slices
    if len(slices)>2*slice_per_line: 
      target=2*slice_per_line # we want 2 lines
    elif len(slices)>slice_per_line:
      target=slice_per_line # or 1 line
    else: target=len(slices) # or just all all slices
    if len(slices)==0: print ("Error: no ROI overlap found")
    else:
      step = int(len(slices)/target)
      start = int((len(slices)-target*step)/2)
      slices = slices[start::step]
      slices = slices [0:target]
       
    height=width * data0.shape[0]/data0.shape[1] * SpatResol[0]/SpatResol[1]
    i=0; ypos=yoffset    
    for slice in slices:
        imgdata0 = data0[:,:,slice]/np.max(data0)*255
        imgdata0 = imgdata0.astype(np.uint8)
        imgdata0  = lut_gray[imgdata0]
        imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
        imgdata0[:,:,3]=255 # but don't use it
        img0 = Image.fromarray(imgdata0)
        
        imgdata1 = data1[:,:,slice]/np.max(data1)*255
        imgdata1 = imgdata1.astype(np.uint8)
        imgdata1  = lut_left[imgdata1]
        imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data1[:,:,slice]/np.max(data1)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata1[:,:,3] = alpha 
        img1 = Image.fromarray(imgdata1)

        imgdata2 = data2[:,:,slice]/np.max(data2)*255
        imgdata2 = imgdata2.astype(np.uint8)
        imgdata2  = lut_right[imgdata2]
        imgdata2 = np.append (imgdata2, np.zeros([imgdata2.shape[0],imgdata2.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data2[:,:,slice]/np.max(data2)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata2[:,:,3] = alpha 
        img2 = Image.fromarray(imgdata2)    
        
        img0.paste(img1, (0,0), img1)
        img0.paste(img2, (0,0), img2)
        img0 = img0.convert ("RGB") # remove alpha channel
        if fpdf_version<"2": #old version, write on disk
          tempfile = '.overlay_axi'+str(slice)+'.png'
          img0.save(tempfile)
        else: #new version, write in memory
          tempfile = BytesIO()
          img0.save(tempfile, 'png')
          tempfile.name = 'test.png'
          tempfile.seek(0)
        xpos=(i%slice_per_line)*width + xoffset
        ypos=int(i/slice_per_line)*height + yoffset
        pdf.image(tempfile, x = xpos, y=ypos, w = width, h=height, type="png")
        if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile    
        i += 1

    yoffset=ypos+height+sparator

    # --------------------------------------- CORONAL ----------------------------------------------

    #add some black in Z
    npoints=int(data0.shape[2]*0.05)
    zeros = np.zeros ([data0.shape[0],data0.shape[1],npoints])
    data0 = np.append(zeros,data0,axis=2); data0 = np.append(data0,zeros,axis=2)
    data1 = np.append(zeros,data1,axis=2); data1 = np.append(data1,zeros,axis=2)
    data2 = np.append(zeros,data2,axis=2); data2 = np.append(data2,zeros,axis=2)

    # transformations
    data0 = np.rot90(data0, axes=(1,2))
    data1 = np.rot90(data1, axes=(1,2))
    data2 = np.rot90(data2, axes=(1,2))
    SpatResol[2], SpatResol[1] = SpatResol[1], SpatResol[2]

    # find all slices that contain some part of either ROI 
    slices=[]; npoints=[]
    thresh = int(0.001*data0.shape[1]*data0.shape[2])
    for slice in range (0,data0.shape[0]):
      nz1=np.nonzero(data1[slice,:,:])
      nz2=np.nonzero(data2[slice,:,:])
      if len(nz1[0])>thresh and len(nz2[0])>thresh: slices.append(slice); npoints.append(len(nz1[0]))
      
    # choose a subset of these slices
    if len(slices)>2*slice_per_line: 
      target=2*slice_per_line # we want 2 lines
    elif len(slices)>slice_per_line:
      target=slice_per_line # or 1 line
    else: target=len(slices) # or just all all slices
    if len(slices)==0: print ("Error: no ROI overlap found")
    else:
      step = int(len(slices)/target)
      start = int((len(slices)-target*step)/2)
      slices = slices[start::step]
      slices = slices [0:target]
     
    height=width * data0.shape[1]/data0.shape[2] * SpatResol[1]/SpatResol[2]
    i=0; ypos=yoffset     
    for slice in slices:
        imgdata0 = data0[slice,:,:]/np.max(data0)*255
        imgdata0 = imgdata0.astype(np.uint8)
        imgdata0  = lut_gray[imgdata0]
        imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
        imgdata0[:,:,3]=255 # but don't use it
        img0 = Image.fromarray(imgdata0)
        
        imgdata1 = data1[slice,:,:]/np.max(data1)*255
        imgdata1 = imgdata1.astype(np.uint8)
        imgdata1  = lut_left[imgdata1]
        imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data1[slice,:,:]/np.max(data1)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata1[:,:,3] = alpha 
        img1 = Image.fromarray(imgdata1)

        imgdata2 = data2[slice,:,:]/np.max(data2)*255
        imgdata2 = imgdata2.astype(np.uint8)
        imgdata2  = lut_right[imgdata2]
        imgdata2 = np.append (imgdata2, np.zeros([imgdata2.shape[0],imgdata2.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data2[slice,:,:]/np.max(data2)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata2[:,:,3] = alpha 
        img2 = Image.fromarray(imgdata2)    
        
        
        img0.paste(img1, (0,0), img1)
        img0.paste(img2, (0,0), img2)
        img0 = img0.convert ("RGB") # remove alpha channel
        if fpdf_version<"2": #old version, write on disk
          tempfile = '.overlay_cor'+str(slice)+'.png'
          img0.save(tempfile)
        else: #new version, write in memory
          tempfile = BytesIO()
          img0.save(tempfile, 'png')
          tempfile.name = 'test.png'
          tempfile.seek(0)    
        xpos=(i%slice_per_line)*width + xoffset
        ypos=int(i/slice_per_line)*height + yoffset
        pdf.image(tempfile, x = xpos, y=ypos, w = width, h=height, type="png")
        if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile  
        i += 1
        
    yoffset=ypos+height+sparator 

    # --------------------------------------- SAGITAL RIGHT ----------------------------------------

    # transformations
    data0 = np.rot90(data0, axes=(0,1),k=3)
    data1 = np.rot90(data1, axes=(0,1),k=3)
    data2 = np.rot90(data2, axes=(0,1),k=3)
    SpatResol[1], SpatResol[0] = SpatResol[0], SpatResol[1]

    # find all slices that contain some part of either ROI 
    slices=[]; npoints=[]
    thresh = int(0.001*data0.shape[0]*data0.shape[1])
    for slice in range (0,data0.shape[2]):
      nz2=np.nonzero(data2[:,:,slice])
      if len(nz2[0])>thresh: slices.append(slice); npoints.append(len(nz1[0]))
      
    # choose a subset of these slices
    if len(slices)>slice_per_line:
      target=slice_per_line # or 1 line
    else: target=len(slices) # or just all all slices
    if len(slices)==0: print ("Error: no ROI overlap found")
    else:
      step = int(len(slices)/target)
      start = int((len(slices)-target*step)/2)
      slices = slices[start::step]
      slices = slices [0:target]

    height=width * data0.shape[0]/data0.shape[1] * SpatResol[0]/SpatResol[1]
    i=0; ypos=yoffset     
    for slice in slices:
        imgdata0 = data0[:,:,slice]/np.max(data0)*255
        imgdata0 = imgdata0.astype(np.uint8)
        imgdata0  = lut_gray[imgdata0]
        imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
        imgdata0[:,:,3]=255 # but don't use it
        img0 = Image.fromarray(imgdata0)
        
        imgdata2 = data2[:,:,slice]/np.max(data2)*255
        imgdata2 = imgdata2.astype(np.uint8)
        imgdata2  = lut_right[imgdata2]
        imgdata2 = np.append (imgdata2, np.zeros([imgdata2.shape[0],imgdata2.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data2[:,:,slice]/np.max(data2)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata2[:,:,3] = alpha 
        img2 = Image.fromarray(imgdata2)    
        
        img0.paste(img2, (0,0), img2)
        img0 = img0.convert ("RGB") # remove alpha channel
        if fpdf_version<"2": #old version, write on disk
          tempfile = '.overlay_sag'+str(slice)+'.png'
          img0.save(tempfile)
        else: #new version, write in memory
          tempfile = BytesIO()
          img0.save(tempfile, 'png')
          tempfile.name = 'test.png'
          tempfile.seek(0)    
        xpos=(i%slice_per_line)*width + xoffset
        ypos=int(i/slice_per_line)*height + yoffset
        pdf.image(tempfile, x = xpos, y=ypos, w = width, h=height, type="png")
        if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile  
        i += 1
        
    yoffset=ypos+height    

    # --------------------------------------- SAGITAL LEFT ----------------------------------------

    # find all slices that contain some part of either ROI 
    slices=[]; npoints=[]
    thresh = int(0.001*data0.shape[0]*data0.shape[1])
    for slice in range (0,data0.shape[2]):
      nz1=np.nonzero(data1[:,:,slice])
      if len(nz1[0])>thresh: slices.append(slice); npoints.append(len(nz1[0]))

      
    # choose a subset of these slices
    if len(slices)>slice_per_line:
      target=slice_per_line # or 1 line
    else: target=len(slices) # or just all all slices
    if len(slices)==0: print ("Error: no ROI overlap found")
    else:
      step = int(len(slices)/target)
      start = int((len(slices)-target*step)/2)
      slices = slices[start::step]
      slices = slices [0:target]    

    #invert slice order
    slices = slices[::-1]

    height=width * data0.shape[0]/data0.shape[1] * SpatResol[0]/SpatResol[1]
    i=0; ypos=yoffset     
    for slice in slices:
        imgdata0 = data0[:,:,slice]/np.max(data0)*255
        imgdata0 = imgdata0.astype(np.uint8)
        imgdata0  = lut_gray[imgdata0]
        imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
        imgdata0[:,:,3]=255 # but don't use it
        img0 = Image.fromarray(imgdata0)
        
        imgdata1 = data1[:,:,slice]/np.max(data1)*255
        imgdata1 = imgdata1.astype(np.uint8)
        imgdata1  = lut_left[imgdata1]
        imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
        alpha = data1[:,:,slice]/np.max(data1)*255*transparancy
        alpha = alpha.astype(np.uint8)
        imgdata1[:,:,3] = alpha 
        img1 = Image.fromarray(imgdata1)
       
        img0.paste(img1, (0,0), img1)
        img0 = img0.convert ("RGB") # remove alpha channel
        if fpdf_version<"2": #old version, write on disk
          tempfile = '.overlay_sag'+str(slice)+'.png'
          img0.save(tempfile)
        else: #new version, write in memory
          tempfile = BytesIO()
          img0.save(tempfile, 'png')
          tempfile.name = 'test.png'
          tempfile.seek(0)    
        xpos=(i%slice_per_line)*width + xoffset
        ypos=int(i/slice_per_line)*height + yoffset
        pdf.image(tempfile, x = xpos, y=ypos, w = width, h=height, type="png")
        if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile  
        i += 1
        
    pdf.output(filename)




def main():

    # get input filename
    if len(sys.argv)==2: filename=sys.argv[1]
    elif len(sys.argv)==1: filename = GetFilename()
    else: print ("Usage:",sys.argv[0],"[NIFTI_Image]"); sys.exit(2)

    #read data
    try: img0 = nib.load(filename)
    except: basename = os.path.basename(filename); print ("Error reading "+basename); sys.exit(2)
    data0 = np.asanyarray(img0.dataobj).astype(np.float32)
    dirname  = os.path.dirname(filename)
    basename = os.path.splitext(os.path.splitext(os.path.basename(filename))[0])[0]
    SpatResol = np.asarray(img0.header.get_zooms())
    
    try: img1 = nib.load(os.path.join(dirname,basename+"_mask_L.nii.gz"))
    except: print ("Error reading "+basename+"_mask_L.nii.gz"); sys.exit(2)
    data1 = np.asanyarray(img1.dataobj).astype(np.float32)
    data1 /= np.max(data1) # normalize to 1.0

    try: img2 = nib.load(os.path.join(dirname,basename+"_mask_R.nii.gz"))
    except: print ("Error reading "+basename+"_mask_R.nii.gz"); sys.exit(2)
    data2 = np.asanyarray(img2.dataobj).astype(np.float32)
    data2 /= np.max(data2) # normalize to 1.0

    try: img3 = nib.load(os.path.join(dirname,basename+"_brain_mask.nii.gz"))
    except: print ("Error reading "+basename+"_brain_mask.nii.gz"); sys.exit(2)
    data3 = np.asanyarray(img3.dataobj).astype(np.float32)
    #data3 /= np.max(data3) # normalize to 1.0    

    o1 = nib.orientations.io_orientation(img0.affine)
    o2 = np.array([[ 0., -1.], [ 1.,  1.], [ 2.,  1.]]) # We work in LAS space (same as the mni_icbm152 template)
    trn = nib.orientations.ornt_transform(o1, o2) # o1 to o2 (apply to o2 to obtain o1)
    data0 = nib.apply_orientation(data0, trn )
    data1 = nib.apply_orientation(data1, trn )
    data2 = nib.apply_orientation(data2, trn )
    data3 = nib.apply_orientation(data3, trn )
    SpatResol[int(trn[0,0])],  SpatResol[int(trn[1,0])], SpatResol[int(trn[2,0])] = SpatResol[0],  SpatResol[1], SpatResol[2]

    
    try: 
      with open(os.path.join(dirname,basename+"_hippoLR_volumes.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
          line_count += 1
          if line_count == 2:
            vol      = float(row[0])
            volsAA_L = float(row[1])
            volsAA_R = float(row[2])
    except: print ("Error reading "+basename+"_hippoLR_volumes.csv"); sys.exit(2)
    
    text0 = "HippoDeep Report"
    text1="Total Intracranial Volume:  "
    text2="Left  Hippocampus  Volume:  "
    text3="Right Hippocampus  Volume:  "
    text1 += "{:.2f}".format(float(vol)/1000000,2)+" l" # transform mm^3 to liter
    text2 += "{:.2f}".format(float(volsAA_L)/1000,2)+" ml" # transform mm^3 to mililiter   
    text3 += "{:.2f}".format(float(volsAA_R)/1000,2)+" ml" # transform mm^3 to mililiter
    filename = os.path.join(dirname,basename+".pdf")
    HippoDeepReport (SpatResol,data0, data1, data2, data3, text0, text1, text2, text3, filename)

    #end
    if sys.platform=="win32": os.system("pause") # windows
        
if __name__ == '__main__':
    main()        
        
