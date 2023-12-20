#ifndef _CUSKETCH_H
#define _CUSKETCH_H

#include "params.h"
#include "BOBHash32.h"
#include <cstring>
#include <algorithm>

using namespace std;

template <int memory_in_bytes, int d>
class SlidingCUSketch
{
private:
    static constexpr int w = memory_in_bytes * 8 / 32;
	int counters[w][2], morning;
	BOBHash32 * hash[d];
public:
    SlidingCUSketch()
    {
        memset(counters, 0, sizeof(counters));
        for (int i = 0; i < d; i++)
            hash[i] = new BOBHash32(i + 750);
    }

    void print_basic_info()
    {
        printf("CU sketch\n");
        printf("\tCounters: %d\n", w);
        printf("\tMemory: %.6lfMB\n", w * 4.0 / 1024 / 1024);
    }

    virtual ~SlidingCUSketch()
    {
        for (int i = 0; i < d; i++)
            delete hash[i];
    }

    void insert(uint32_t key, int f = 1)
    {
        int index[d];
        int value[d];
        int min_val = 1 << 30;

        for (int i = 0; i < d; i++) {
            index[i] = (hash[i]->run((const char *)&key, 4)) % w;
            value[i] = counters[index[i]][0];
            min_val = min(min_val, value[i]);
        }

        int temp = min_val + f;
        for (int i = 0; i < d; i++) {
            counters[index[i]][0] = max(counters[index[i]][0], temp);
        }
    }

	int query(uint32_t key)
    {
        int ret = 1 << 30;
        for (int i = 0; i < d; i++) {
            int index = (hash[i]->run((const char *)&key, 4)) % w;
            int tmp = counters[index][0] + counters[index][1];
            ret = min(ret, tmp);
        }
        return ret;
    }

    void tick() {
        counters[morning][1] = counters[morning][0];
        counters[morning][0] = 0;
        morning = (morning + 1) % w;
    }

    int batch_query(uint32_t * data, int n) {
        int ret = 0;
        for (int i = 0; i < n; ++i) {
            ret += query(data[i]);
        }
        return ret;
    }

    void build(uint32_t * data, int n)
    {
        for (int i = 0; i < n; ++i) {
            insert(data[i], 1);
        }
    }
};

#endif //_CUSKETCH_H