#include <stdlib.h>
#include "gd.h"
#include "gdtest.h"

int
main(void)
{
	gdImagePtr im;
	int white, black, r;
	gdPointPtr points;

	im = gdImageCreate(100, 100);
	if (!im) exit(EXIT_FAILURE);
	white = gdImageColorAllocate(im, 0xff, 0xff, 0xff);
	black = gdImageColorAllocate(im, 0, 0, 0);
	gdImageFilledRectangle(im, 0, 0, 99, 99, white);
	points = (gdPointPtr)gdCalloc(3, sizeof(gdPoint));
	if (!points) {
		gdImageDestroy(im);
		exit(EXIT_FAILURE);
	}
	points[0].x = 10;
	points[0].y = 10;
	points[1].x = 50;
	points[1].y = 70;
	points[2].x = 90;
	points[2].y = 30;
	gdImagePolygon(im, points, 3, black);

	gdFree(points);
	gdImageDestroy(im);

	return EXIT_SUCCESS;
}
