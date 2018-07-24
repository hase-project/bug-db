#include "sqlite3.h"

int main() {
    sqlite3_mprintf("%*.*f", 2000000000, 1000000000, 1.0e-20);
}