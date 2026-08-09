<template>

<Layout>

    <template #sidebar>
        <StaffSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">Welcome, Staff</h2>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading dashboard...</p>
    </div>

    <!-- Stats -->
    <div v-if="!loading" class="row mb-4">

        <div class="col-md-4">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">🏔</div>
                    <h6 class="text-muted">Assigned Treks</h6>
                    <h2>{{ stats.assigned_treks || 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">✅</div>
                    <h6 class="text-muted">Completed Treks</h6>
                    <h2>{{ stats.completed_treks || 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card shadow-sm border-0">
                <div class="card-body text-center">
                    <div class="fs-2">📊</div>
                    <h6 class="text-muted">Total Participants</h6>
                    <h2>{{ totalParticipants }}</h2>
                </div>
            </div>
        </div>

    </div>

    <!-- Assigned treks quick list -->
    <div v-if="!loading">

        <h5 class="mb-3">Assigned Treks</h5>

        <table class="table table-bordered table-hover">
            <thead class="table-success">
                <tr>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Slots Available</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="trek in treks" :key="trek.id">
                    <td>{{ trek.name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>
                        <span :class="statusBadge(trek.status)">{{ trek.status }}</span>
                    </td>
                    <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
                    <td>
                        <RouterLink :to="`/staff/treks/${trek.id}`" class="btn btn-outline-success btn-sm">
                            View
                        </RouterLink>
                    </td>
                </tr>
                <tr v-if="!treks.length">
                    <td colspan="5" class="text-center text-muted py-4">No treks assigned yet.</td>
                </tr>
            </tbody>
        </table>

    </div>

</Layout>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import StaffSidebar from "../../components/staff/StaffSidebar.vue";
import api from "../../services/api";

const stats = ref({});
const treks = ref([]);
const loading = ref(true);
const error = ref("");

const totalParticipants = computed(() => {
    return treks.value.reduce((sum, t) => {
        return sum + (t.total_slots - t.available_slots);
    }, 0);
});

function statusBadge(status) {
    const map = {
        PENDING: "badge bg-secondary",
        APPROVED: "badge bg-info text-dark",
        OPEN: "badge bg-success",
        CLOSED: "badge bg-warning text-dark",
        COMPLETED: "badge bg-primary"
    };
    return map[status] || "badge bg-secondary";
}

async function load() {

    loading.value = true;

    try {
        const [dashRes, treksRes] = await Promise.all([
            api.get("/staff/dashboard"),
            api.get("/staff/treks")
        ]);

        stats.value = dashRes.data.statistics || {};
        treks.value = treksRes.data.treks;
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