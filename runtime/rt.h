#ifndef RT_H
#define RT_H

typedef enum { T_INT } Tag;

typedef struct {
    Tag tag;
    union { long i; } as;
} Value;

Value rt_int(long n);
Value rt_add(Value a, Value b);
Value rt_sub(Value a, Value b);
Value rt_mul(Value a, Value b);
Value rt_div(Value a, Value b);
void  rt_print(Value v);
void  rt_panic(const char *msg);

#endif
