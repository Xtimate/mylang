#include "rt.h"

int main(void) {
    Value v_n_0 = rt_int(0);
    while (rt_truthy(rt_lt(rt_use(&v_n_0, "n"), rt_int(3)))) {
        Value v_s_1 = rt_str("hi");
        rt_print(rt_use(&v_s_1, "s"));
        { Value t = rt_add(rt_use(&v_n_0, "n"), rt_int(1)); rt_drop(&v_n_0); v_n_0 = t; }
        rt_drop(&v_s_1);
    }
    rt_drop(&v_n_0);
    return 0;
}

