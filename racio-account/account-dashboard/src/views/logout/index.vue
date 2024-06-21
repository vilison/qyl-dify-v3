<template>
    <div class="logout"></div>
</template>

<script lang="ts" setup>

import { useUserStore } from "@/store/modules/user"
import { useRouter } from "vue-router"
const router = useRouter()
const user = useUserStore()
user.logout()
router.replace({ path: "/" })

</script>
