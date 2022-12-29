#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>

#include <string>
#include <fstream>
#include <sstream>
#include <list>
#include <vector>
#include <algorithm>
#include <set>
#include <map>

#include <smmintrin.h>

/*
 * That's way too slow, and it does not validate the test sample for the 2nd part :(
 */

// 4x32 bits
// (ore, clay, obsidian, geode)
typedef uint32_t v4su __attribute__((vector_size(16))); // 4x32 bits

struct Blueprint {
    v4su ore;
    v4su clay;
    v4su obsidian;
    v4su geode;
    unsigned int n;
} __attribute__((aligned(16)));

struct State {
    v4su stock;
    v4su production;
    unsigned int rem;
    
    State() {}

    bool operator<(const State &o) const {
        return ::memcmp(this, &o, sizeof(State)) < 0;
    }
    bool operator==(const State &o) const {
        return ::memcmp(this, &o, sizeof(State)) == 0;
    }
} __attribute__((aligned(16)));

bool parse_input(const std::string &filename, std::list<Blueprint> &blueprints) {
    std::ifstream in(filename);
    if (!in.is_open()) {
        fprintf(stderr, "Fichier '%s' non ouvert\n", filename.c_str());
        return false;
    }
    blueprints.clear();

    for (std::string line; std::getline(in, line); ) {
        std::vector<unsigned int> numbers;
        std::istringstream iss(line);
        for (std::string word; std::getline(iss, word, ' '); ) {
            try {
                unsigned int n = std::stoul(word);
                numbers.push_back(n);
            }
            catch (...) {}
        }
        Blueprint bp;
        bp.n = numbers[0];
        bp.ore = v4su{numbers[1], 0, 0, 0};
        bp.clay = v4su{numbers[2], 0, 0, 0};
        bp.obsidian = v4su{numbers[3], numbers[4], 0, 0};
        bp.geode = v4su{numbers[5], 0, numbers[6], 0};
        blueprints.push_back(bp);
    }

    return true;
}

class Simu {
    Blueprint bp;
    uint32_t max_ore_robots;
    uint32_t max_clay_robots;
    uint32_t max_obsidian_robots;

    bool can_build_ore_robot(const State &s) const {
        if (s.production[0] >= max_ore_robots) {
            return false;
        }
        v4su t = s.stock < bp.ore;
        return _mm_test_all_zeros((__m128i) t, (__m128i) t);
    }
    
    bool can_build_clay_robot(const State &s) const {
        if (s.production[1] >= max_clay_robots) {
            return false;
        }
        v4su t = s.stock < bp.clay;
        return _mm_test_all_zeros((__m128i) t, (__m128i) t);
    }

    bool can_build_obsidian_robot(const State &s) const {
        if (s.production[2] >= max_obsidian_robots) {
            return false;
        }
        v4su t = s.stock < bp.obsidian;
        return _mm_test_all_zeros((__m128i) t, (__m128i) t);
    }

    bool can_build_geode_robot(const State &s) const {
        v4su t = s.stock < bp.geode;
        return _mm_test_all_zeros((__m128i) t, (__m128i) t);
    }


public:
    Simu(const Blueprint &bp_) : bp(bp_) {
        max_ore_robots = std::max(bp.ore[0], bp.clay[0]);
        max_ore_robots = std::max(max_ore_robots, bp.obsidian[0]);
        max_ore_robots = std::max(max_ore_robots, bp.geode[0]);
        max_clay_robots = bp.obsidian[1];
        max_obsidian_robots = bp.geode[2];
    }

    inline bool round_do_nothing(const State &s, State &r) const {
        r = s;
        r.stock += s.production;
        r.rem -= 1;
        return true;
    }

    inline bool round_build_ore(const State &s, State &r) const {
        if (can_build_ore_robot(s)) {
            r = s;
            r.stock = r.stock - bp.ore + s.production;
            r.production += v4su{1,0,0,0};
            r.rem -= 1;
            return true;
        }
        return false;
    }

    inline bool round_build_clay(const State &s, State &r) const {
        if (can_build_clay_robot(s)) {
            r = s;
            r.stock = r.stock - bp.clay + s.production;
            r.production += v4su{0,1,0,0};
            r.rem -= 1;
            return true;
        }
        return false;
    }

    inline bool round_build_obsidian(const State &s, State &r) const {
        if (can_build_obsidian_robot(s)) {
            r = s;
            r.stock = r.stock - bp.obsidian + s.production;
            r.production += v4su{0,0,1,0};
            r.rem -= 1;
            return true;
        }
        return false;
    }

    inline bool round_build_geode(const State &s, State &r) const {
        if (can_build_geode_robot(s)) {
            r = s;
            r.stock = r.stock - bp.geode + s.production;
            r.production += v4su{0,0,0,1};
            r.rem -= 1;
            return true;
        }
        return false;
    }
};

static void part_1_2(const std::string &filename, bool part2 = false) {
    std::list<Blueprint> blueprints;
    if (!parse_input(filename, blueprints)) {
        return;
    }

    if (part2) {
        if (blueprints.size() > 3) {
            blueprints.resize(3);
        }
    }
    
    uint64_t ret = part2 ? 1 : 0;
    State init_state;
    init_state.stock = v4su{0,0,0,0};
    init_state.production = v4su{1,0,0,0};
    init_state.rem = part2 ? 32 : 24;
    std::vector<State> stack(64); // fixed stack
    for (const auto &bp: blueprints) {
        uint32_t stack_p = 0;
        stack[stack_p] = init_state;
        ++stack_p;
        Simu simu(bp);

        printf("%u : (%u) (%u) (%u,%u), (%u,%u)\n", bp.n, bp.ore[0], bp.clay[0], bp.obsidian[0], bp.obsidian[1], bp.geode[0], bp.geode[2]);

        std::vector<uint32_t> best_geodes_at_rem(init_state.rem + 1);
        uint64_t best_geode = 0;
        while (stack_p != 0) {
            State state = stack[--stack_p];

            if (state.rem == 0) {
                uint32_t g = state.stock[3];
                if (g > best_geode) {
                    best_geode = g;
                    // printf("  best bp %u: %u\n", bp.n, g);
                }
                continue;
            }

            if (state.stock[3] < best_geodes_at_rem[state.rem]) {
                continue;
            }
            else if (state.stock[3] > best_geodes_at_rem[state.rem]) {
                best_geodes_at_rem[state.rem] = state.stock[3];
            }

            if (simu.round_build_geode(state, stack[stack_p])) {
                ++stack_p;
                continue;
            }
            if (simu.round_build_obsidian(state, stack[stack_p])) {
                ++stack_p;
            }
            if (simu.round_do_nothing(state, stack[stack_p])) {
                ++stack_p;
            }
            if (simu.round_build_ore(state, stack[stack_p])) {
                ++stack_p;
            }
            if (simu.round_build_clay(state, stack[stack_p])) {
                ++stack_p;
            }
        }

        if (part2) {
            ret *= best_geode;
        }
        else {
            ret += bp.n * best_geode;
        }
    }
    printf("** %s: %lu\n", part2?"part2":"part1", ret);
}

// static uint32_t work_rec(const Simu &simu, const State &state, std::map<uint32_t, uint32_t> &best_geoms_at_rem) {
//     if (state.rem == 0) {
//         return state.stock[3];
//     }
// 
//     uint32_t g = state.stock[3];
//     if (g < best_geoms_at_rem[state.rem]) {
//         return 0;
//     }
//     else if (g > best_geoms_at_rem[state.rem]) {
//         best_geoms_at_rem[state.rem] = g;
//     }
// 
//     uint32_t best = 0;
//     State nstate;
//     if (simu.round_build_geode(state, nstate)) {
//         return work_rec(simu, nstate, best_geoms_at_rem);
//     }
//     else {
//         if (simu.round_build_obsidian(state, nstate)) {
//             best = std::max(best, work_rec(simu, nstate, best_geoms_at_rem));
//         }
//         if (simu.round_build_clay(state, nstate)) {
//             best = std::max(best, work_rec(simu, nstate, best_geoms_at_rem));
//         }
//         if (simu.round_build_ore(state, nstate)) {
//             best = std::max(best, work_rec(simu, nstate, best_geoms_at_rem));
//         }
//         if (simu.round_do_nothing(state, nstate)) {
//             best = std::max(best, work_rec(simu, nstate, best_geoms_at_rem));
//         }
//         return best;
//     }
// }
// 
// static void part_1_2_rec(const std::string &filename, bool part2 = false) {
//     std::list<Blueprint> blueprints;
//     if (!parse_input(filename, blueprints)) {
//         return;
//     }
// 
//     if (part2) {
//         if (blueprints.size() > 3) {
//             blueprints.resize(3);
//         }
//     }
//     
//     uint64_t ret = part2 ? 1 : 0;
//     State init_state;
//     init_state.stock = v4su{0,0,0,0};
//     init_state.production = v4su{1,0,0,0};
//     init_state.rem = part2 ? 32 : 24;
//     for (const auto &bp: blueprints) {
//         Simu simu(bp);
// 
//         printf("%u : (%u) (%u) (%u,%u), (%u,%u)\n", bp.n, bp.ore[0], bp.clay[0], bp.obsidian[0], bp.obsidian[1], bp.geode[0], bp.geode[2]);
//         std::map<uint32_t, uint32_t> cache;
//         for (unsigned int i = 0; i <= init_state.rem; ++i) {cache[i] = 0;}
//         uint64_t b = work_rec(simu, init_state, cache);
//         if (part2) {
//             ret *= b;
//         }
//         else {
//             ret += bp.n * b;
//         }
//     }
//     printf("** %s: %lu\n", part2?"part2":"part1", ret);
// }

int main(int argc, char **argv) {
    const char *opt_filename = "input_19";
    if (argc > 1) {
        opt_filename = argv[1];
    }

    part_1_2(opt_filename);
    part_1_2(opt_filename, true);

    return 0;
}
