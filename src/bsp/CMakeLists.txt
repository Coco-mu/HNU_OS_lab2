set(SRCS start.S prt_reset_vector.S print.c vsnprintf_s.c)
add_library(bsp OBJECT ${SRCS})
