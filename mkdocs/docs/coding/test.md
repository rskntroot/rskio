
# IPADDR

## Brief

A naive attempt at optimizing an ipv4 address with only std::env

Note, using `strace` to judge efficacy not a valid approach.
 I ended up trying a couple different tests, but need to work on better methodology.

## Assumptions

=== "Cargo.tml"

  ``` toml
  [profile.release]
  strip = "symbols"
  debug = 0
  opt-level = "z"
  lto = true
  codegen-units = 1
  panic = "abort"
  ```

## Code

### Unoptimized

- Stores args as an immutable (imut) string vector
- Stores `ip_addr` as imut string then shadows as imut string slice vector
- Uses len() calls for no real reason

=== "main.rs"

    ``` rust
    use std::env;

    fn main() {
        let args: Vec<String> = env::args().collect();
        if args.len() > 1 {
            let ip_addr: String = args[1].to_string();
            let ip_addr: Vec<&str> = ip_addr.split('.').collect();
            if ip_addr.len() == 4 {
                for octect in ip_addr {
                    octect.parse::<u8>().expect(&format!("invalid ip"));
                }
            } else {
                panic!("invalid ip")
            }
        }
    }
    ```

=== "strace"

    ``` zsh
    ~/workspace/ipcheck> sha256sum src/main.rs
    4cb6865ea743c3a2cee6e05966e117b8db51f32cb55de6baad205196bbc4195d  src/main.rs

    ~/workspace/ipcheck> cargo build --release
    Compiling ipcheck v0.1.0 (/home/lost/workspace/ipcheck)
        Finished `release` profile [optimized] target(s) in 2.93s

    ~/workspace/ipcheck> strace -c ./target/release/ipcheck 1.1.1.1
    % time     seconds  usecs/call     calls    errors syscall
    ------ ----------- ----------- --------- --------- ------------------
    37.07    0.000470         470         1           execve
    14.43    0.000183          14        13           mmap
    8.52    0.000108          21         5           read
    7.10    0.000090          15         6           mprotect
    6.78    0.000086          21         4           openat
    3.63    0.000046          23         2           munmap
    3.08    0.000039           9         4           newfstatat
    2.76    0.000035          11         3           brk
    2.60    0.000033           6         5           rt_sigaction
    2.52    0.000032           8         4           close
    2.37    0.000030           7         4           pread64
    1.50    0.000019           6         3           sigaltstack
    1.34    0.000017          17         1         1 access
    1.34    0.000017           8         2           prlimit64
    1.10    0.000014           7         2         1 arch_prctl
    1.03    0.000013          13         1           poll
    0.71    0.000009           9         1           sched_getaffinity
    0.63    0.000008           8         1           getrandom
    0.55    0.000007           7         1           set_tid_address
    0.47    0.000006           6         1           set_robust_list
    0.47    0.000006           6         1           rseq
    ------ ----------- ----------- --------- --------- ------------------
    100.00    0.001268          19        65         2 total
    ```


### Optimized

- Needs some cleanup
- Needs break for args after index 1

=== "main.rs"

    ``` rust
    use std::env;

    fn main() {
        for (index, arg) in env::args().enumerate(){
            if index == 1 {
                for (i, octect) in arg.split('.').collect::<Vec<&str>>().iter().enumerate() {
                    if i > 3 {
                        panic!("invalid")
                    } else {
                        let _ = &octect.parse::<u8>().expect("invalid");
                    }
                }
            }
        }
    }
    ```

=== "strace"

    ``` zsh
    ~/workspace/ipcheck> sha256sum src/main.rs
    838b3f0c99448e8bbe88001de4d12f5062d293a2a1fd236deacfabdb30a7e2e4  src/main.rs

    ~/workspace/ipcheck> cargo build --release
    Compiling ipcheck v0.1.0 (/home/lost/workspace/ipcheck)
        Finished `release` profile [optimized] target(s) in 2.89s

    ~/workspace/ipcheck> strace -c ./target/release/ipcheck 1.1.1.1                                                                                                                      06/22/2024 07:57:31 PM
    % time     seconds  usecs/call     calls    errors syscall
    ------ ----------- ----------- --------- --------- ------------------
    23.07    0.000161          12        13           mmap
    15.33    0.000107          21         5           read
    13.04    0.000091          15         6           mprotect
    10.17    0.000071          17         4           openat
    6.73    0.000047          23         2           munmap
    4.87    0.000034           6         5           rt_sigaction
    4.01    0.000028           7         4           pread64
    4.01    0.000028           7         4           newfstatat
    3.72    0.000026           6         4           close
    2.87    0.000020           6         3           sigaltstack
    2.15    0.000015           5         3           brk
    2.01    0.000014          14         1           poll
    1.86    0.000013           6         2           prlimit64
    1.29    0.000009           9         1           sched_getaffinity
    1.15    0.000008           8         1           getrandom
    1.00    0.000007           3         2         1 arch_prctl
    1.00    0.000007           7         1           set_tid_address
    0.86    0.000006           6         1           set_robust_list
    0.86    0.000006           6         1           rseq
    0.00    0.000000           0         1         1 access
    0.00    0.000000           0         1           execve
    ------ ----------- ----------- --------- --------- ------------------
    100.00    0.000698          10        65         2 total
    ```
