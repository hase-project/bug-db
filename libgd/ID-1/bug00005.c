#include <gd.h>

int main()
{
 	gdImagePtr im;
	FILE *fp;


	fp = fopen("bug00005_2.gif", "rb");

	im = gdImageCreateFromGif(fp);

	if (!im) {
	  fprintf(stderr, "%s Invalid GIF file\n", "bug00005_2.gif");
	} else {
	  fprintf(stderr, "%s valid GIF file\n", "bug00005_2.gif");
		 gdImageDestroy(im);
	}

 	return 0;
}
