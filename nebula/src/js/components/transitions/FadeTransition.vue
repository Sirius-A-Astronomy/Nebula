<script setup lang="ts"></script>

<template>
    <TransitionGroup name="fade">
        <slot />
    </TransitionGroup>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-move,
.fade-leave-active {
    transition: all 0.5s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-from {
    transform: translateY(10px);
}

.fade-leave-to {
    transform: translateY(-10px);
}

.fade-leave-active {
    position: absolute;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}
</style>
