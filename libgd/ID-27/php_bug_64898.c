#include <stdio.h>
#include <stdlib.h>
#include <gd.h>

int main()
{
	gdImagePtr im, exp;
	char path[2048];
	const char *file_im = "gdinterpolation/php_bug_64898.png";
	FILE *fp;
	int color;

	sprintf(path, "%s/%s", "./", file_im);

	fp = fopen(path, "rb");

	if (!fp) {
		return 1;
	}

	im = gdImageCreateFromPng(fp);

	fclose(fp);

	if (!im) {
		return 1;
	}

	color = gdImageColorAllocate(im, 255, 255, 255);

	if (color < 0) {
		gdFree(im);
		return 1;
	}

/*	Try default interpolation method, but any non-optimized fails */
/*	gdImageSetInterpolationMethod(im, GD_BICUBIC_FIXED); */

	exp = gdImageRotateInterpolated(im, 45, color);

	if (!exp) {
		gdFree(im);
		return 1;
	}

	gdImageDestroy(exp);
	gdImageDestroy(im);

	gdFree(im);

	return 0;
}
