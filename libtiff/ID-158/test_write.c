#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tiffio.h"

unsigned char *
create_test_image(uint16 samples, uint16 bitdepth, uint32 wpix, uint32 hpix)
{
       uint32 stride = ((samples * bitdepth * wpix)+7) / 8;
       unsigned char *buf = (unsigned char*)malloc(stride * hpix);
       unsigned char *bp = buf;
       int state = 1;
       uint32 h, qtrh = hpix/4;
       for (h=0;h<hpix;h++) {
               if (h % qtrh == 0)
                       state = !state;
               memset(bp, (state)?0:0xff, stride);
               bp += stride;
       }
       return buf;
}

int
main(int argc, char **argv)
{
       static uint16 photometrics[] = {
               PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE,
               PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE, PHOTOMETRIC_MINISWHITE,
               PHOTOMETRIC_RGB, PHOTOMETRIC_RGB, PHOTOMETRIC_RGB, PHOTOMETRIC_RGB
       };
       static uint16 bitdepths[] = {
               1, 1, 1, 1, 1,
               8, 8, 8, 8,
               8, 8, 8, 8
       };
       static uint16 compressions[] = {
               COMPRESSION_ADOBE_DEFLATE, COMPRESSION_PACKBITS, COMPRESSION_LZW, COMPRESSION_CCITTFAX3, COMPRESSION_CCITTFAX4,
               COMPRESSION_ADOBE_DEFLATE, COMPRESSION_PACKBITS, COMPRESSION_LZW, COMPRESSION_JPEG,
               COMPRESSION_ADOBE_DEFLATE, COMPRESSION_PACKBITS, COMPRESSION_LZW, COMPRESSION_JPEG
       };

       int i;
       for (i=0; i < sizeof(photometrics)/sizeof(uint16); i++) {
               char *cspace = "unknown";
               if (photometrics[i] == PHOTOMETRIC_MINISWHITE || photometrics[i] == PHOTOMETRIC_MINISBLACK) {
                       if (bitdepths[i] == 1)
                               cspace = "mono";
                       else
                               cspace = "gray";
               } else if (photometrics[i] == PHOTOMETRIC_RGB) {
                       cspace = "rgb";
               } else if (photometrics[i] == PHOTOMETRIC_SEPARATED) {
                       cspace = "cmyk";
               }

               char fn[256];
               sprintf(fn, "test_%s_%d_%d.tif", cspace, bitdepths[i], compressions[i]);

               TIFF *tif = TIFFOpen(fn, "w");
               if (!tif) {
                       puts("ERROR: TIFFOpen failed\n");
                       return 1;
               }

               uint32 hpix = 512, wpix = 512;
               uint16 samples = 1;
               if (photometrics[i] == PHOTOMETRIC_RGB)
                       samples = 3;
               else if (photometrics[i] == PHOTOMETRIC_SEPARATED)
                       samples = 4;
               unsigned char *img = create_test_image(samples, bitdepths[i], wpix, hpix);

               TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
               TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, photometrics[i]);
               TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples);
               TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bitdepths[i]);
               TIFFSetField(tif, TIFFTAG_COMPRESSION, compressions[i]);
               TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, wpix);
               TIFFSetField(tif, TIFFTAG_IMAGELENGTH, hpix);

               uint32 h;
               unsigned char *ip = img;
               for (h=0; h<hpix; h++) {
                       if (TIFFWriteScanline(tif, ip, h, 0) < 0) {
                               puts("ERROR: TIFFWriteScanline failed\n");
                               return 1;
                       }
                       ip += TIFFScanlineSize(tif);
               }

               free(img);
               TIFFClose(tif);
       }
       return 0;
}


