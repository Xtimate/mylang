#include "rt.h"

int main(void) {
    rt_print(rt_div(rt_int(1), rt_int(0)));
    return 0;
}

