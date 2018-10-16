#include <cstdlib>
#include <iostream>
#include <vector>

#include "tiff.h"
#include "tiffio.h"

void print_clump(size_t idx, std::vector<unsigned char> buffer);

int main ( int argc, char *argv[] ) {
    
    TIFF *tif;

    tif = TIFFOpen("quad-tile.jpg.tif","r");
    if ( tif == NULL ) {
        std::cerr << "Could not open " << argv[1] << std::endl;
        exit(-1);
    }

    unsigned short h, v;
    int status = TIFFGetField(tif,TIFFTAG_YCBCRSUBSAMPLING,&h, &v);
    if ( status == 0 ) {
        std::cerr << "Could not retrieve subsampling tag " << std::endl;
        exit(-1);
    }

    fprintf(stdout, "h = %d, v = %d\n", h, v);


    tsize_t sz = TIFFTileSize(tif);
    fprintf(stdout, "tiles are %d bytes\n", sz);

    std::vector<unsigned char> buffer(sz);

    sz = TIFFReadEncodedTile(tif,9,&buffer[0],sz);
    /*
    if (sz == -1) {
        std::cerr << "sz is " << sz << std::endl;
        std::cerr << "Unable to read tile for " << argv[1] << std::endl;
        exit(-1);
    }
    */

    print_clump(0,buffer);
    print_clump(64,buffer);
    print_clump(128,buffer);

    TIFFClose(tif);
    exit ( EXIT_SUCCESS );
}

void print_clump(size_t idx, std::vector<unsigned char> buffer ) {
    for ( size_t j = idx; j < idx+1; ++j ) {
        fprintf(stdout, "clump %d:  \n", j );
        for ( size_t k = 0; k < 4; ++k) {
            fprintf(stdout,"%d ", buffer[j*6 + k]);
        }
        fprintf(stdout,"%d ", buffer[j*6 + 4]);
        fprintf(stdout,"%d ", buffer[j*6 + 5]);
        fprintf(stdout,"\n");
    }
}
