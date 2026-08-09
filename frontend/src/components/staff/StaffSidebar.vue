<template>
<div>
    <p class="fw-semibold text-muted px-2 mb-2 small text-uppercase" style="font-size:0.7rem;letter-spacing:0.08em;">Staff Panel</p>
    <div class="sidebar-nav list-group list-group-flush">
        <RouterLink to="/staff/dashboard" class="list-group-item list-group-item-action" active-class="active">Dashboard</RouterLink>
        <RouterLink to="/staff/treks" class="list-group-item list-group-item-action" active-class="active">My Treks</RouterLink>
    </div>
</div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
