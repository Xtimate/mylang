#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

void rt_panic(const char *msg) {
    fprintf(stderr, "runtime error: %s\n", msg);
    exit(1);
}

Value rt_int(long n) {
    Value v;
    v.tag = T_INT;
    v.as.i = n;
    return v;
}

Value rt_add(Value a, Value b) {
    if (a.tag == T_INT && b.tag == T_INT) return rt_int(a.as.i + b.as.i);
    rt_panic("cannot add these types");
    return rt_int(0);
}

Value rt_sub(Value a, Value b) {
    if (a.tag == T_INT && b.tag == T_INT) return rt_int(a.as.i - b.as.i);
    rt_panic("cannot subtract these types");
    return rt_int(0);
}

Value rt_mul(Value a, Value b) {
    if (a.tag == T_INT && b.tag == T_INT) return rt_int(a.as.i * b.as.i);
    rt_panic("cannot multiply these types");
    return rt_int(0);
}

Value rt_div(Value a, Value b) {
    if (a.tag == T_INT && b.tag == T_INT) {
        if (b.as.i == 0) rt_panic("division by zero");
        return rt_int(a.as.i / b.as.i);
    }
    rt_panic("cannot divide these types");
    return rt_int(0);
}

void rt_print(Value v) {
    switch (v.tag) {
        case T_INT: printf("%ld\n", v.as.i); break;
    }
}
