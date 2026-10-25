@ =============================================================================
@ Function: clear_bss
@ Address:  0x00100024
@ Size:     36 bytes
@ Layer:    ctr/crt
@ Purpose:  CRT startup zeroing loop for the uninitialized data (.bss) section.
@           Iterates from 0x00860934 to 0x0091B9BC, clearing 4 bytes per iteration.
@ =============================================================================

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
