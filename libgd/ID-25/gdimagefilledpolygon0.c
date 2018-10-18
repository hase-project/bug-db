#include <stdlib.h>
#include "gd.h"


int
main(void)
{
	gdImagePtr im;
	int white, black, r;

	im = gdImageCreate(100, 100);
	if (!im) exit(EXIT_FAILURE);
	white = gdImageColorAllocate(im, 0xff, 0xff, 0xff);
	black = gdImageColorAllocate(im, 0, 0, 0);
	gdImageFilledRectangle(im, 0, 0, 99, 99, white);
	gdImageFilledPolygon(im, NULL, 0, black);  /* no effect */
	gdImageFilledPolygon(im, NULL, -1, black); /* no effect */

	gdImageDestroy(im);

	return EXIT_SUCCESS;
}