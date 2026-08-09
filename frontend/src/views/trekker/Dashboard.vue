<template>

<Layout>

    <template #sidebar>
        <TrekkerSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">Welcome, Trekker</h2>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading dashboard...</p>
    </div>

    <!-- Stats -->
    <div v-if="!loading" class="row mb-4">

        <div class="col-md-3">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">🏔</div>
                    <h6 class="text-muted">Available Treks</h6>
                    <h2>{{ availableTreks }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">📋</div>
                    <h6 class="text-muted">My Bookings</h6>
                    <h2>{{ stats.booked_treks || 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">🟢</div>
                    <h6 class="text-muted">Upcoming</h6>
                    <h2>{{ stats.upcoming_treks || 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">✅</div>
                    <h6 class="text-muted">Completed</h6>
                    <h2>{{ stats.completed_treks || 0 }}</h2>
                </div>
            </div>
        </div>

    </div>

    <!-- Quick actions -->
    <div v-if="!loading" class="d-flex gap-3">
        <RouterLink to="/trekker/treks" class="btn btn-success">
            Browse Treks
        </RouterLink>
        <RouterLink to="/trekker/bookings" class="btn btn-outline-secondary">
            View My Bookings
        </RouterLink>
    </div>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import TrekkerSidebar from "../../components/trekker/TrekkerSidebar.vue";
import api from "../../services/api";

const stats = ref({});
const availableTreks = ref(0);
const loading = ref(true);
const error = ref("");

async function load() {

    loading.value = true;

    try {

        const [dashRes, treksRes] = await Promise.all([
            api.get("/trekker/dashboard"),
            api.get("/trekker/treks")
        ]);

        stats.value = dashRes.data.statistics || {};
        availableTreks.value = treksRes.data.treks?.length || 0;

    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load dashboard.";
    }
    finally {
        loading.value = false;
    }

}

onMounted(load);

</script>