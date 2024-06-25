<template>
    <div className="full">
        <div className="relative flex flex-col md:mx-auto md:w-3/4">
            <p className="py-5 text-center text-gray-400">
                &copy; Racio. All rights reserved {{ new Date().getFullYear() }}.
            </p>
        </div>
    </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
.full {
    width: 100%;
    flex: 1;
    text-align: center;
}
</style>
