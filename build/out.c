#include "rt.h"

int main(void) {
    Value v_s = rt_str("one");
    { Value t = rt_str("two"); rt_drop(&v_s); v_s = t; }
    rt_print(rt_use(&v_s, "s"));
    { Value t = rt_str("temp"); rt_print(t); rt_drop(&t); }
    rt_drop(&v_s);
    return 0;
}

