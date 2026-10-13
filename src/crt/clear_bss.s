.arm
.section .text, "ax", %progbits
.global clear_bss
.type clear_bss, %function

clear_bss:
    ldr r0, [pc, #20]
    ldr r1, [pc, #20]
    mov r2, #0
.L_00100030:
    cmp r0, r1
    strcc r2, [r0], #4
    bcc .L_00100030
    bx lr
    .word 0x00860934
    .word 0x0091B9BC

.size clear_bss, . - clear_bss

