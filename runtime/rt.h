#ifndef RT_H
#define RT_H

typedef enum { T_INT, T_STR, T_MOVED } Tag;

typedef struct {
    Tag tag;
    union { long i; char *s; } as;
} Value;

Value rt_int(long n);
Value rt_str(const char *s);
Value rt_use(const Value *v, const char *name);
Value rt_move(Value *v, const char *name);
void  rt_drop(Value *v);
Value rt_add(Value a, Value b);
Value rt_sub(Value a, Value b);
Value rt_mul(Value a, Value b);
Value rt_div(Value a, Value b);
void  rt_print(Value v);
void  rt_panic(const char *msg);

#endif
