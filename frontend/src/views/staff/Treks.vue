<template>

<Layout>

    <template #sidebar>
        <StaffSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">Assigned Treks</h2>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading treks...</p>
    </div>

    <!-- Treks Table -->
    <table v-if="!loading" class="table table-bordered table-hover">

        <thead class="table-success">
            <tr>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th>Slots</th>
                <th>Start Date</th>
                <th>Action</th>
            </tr>
        </thead>

        <tbody>

            <tr v-for="trek in treks" :key="trek.id">
                <td>{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td>
                    <span :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span>
                </td>
                <td>
                    <span :class="statusBadge(trek.status)">{{ trek.status }}</span>
                </td>
                <td>Available: {{ trek.available_slots }} / Total: {{ trek.total_slots }}</td>
                <td>{{ trek.start_date }}</td>
                <td>
                    <RouterLink :to="`/staff/treks/${trek.id}`" class="btn btn-outline-success btn-sm">
                        Manage
                    </RouterLink>
                </td>
            </tr>

            <tr v-if="treks.length === 0">
                <td colspan="7" class="text-center text-muted py-4">No treks assigned to you.</td>
            </tr>

        </tbody>

    </table>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import StaffSidebar from "../../components/staff/StaffSidebar.vue";
import api from "../../services/api";

const treks = ref([]);
const loading = ref(true);
const error = ref("");

function difficultyBadge(difficulty) {
    if (difficulty === "EASY") return "badge bg-success";
    if (difficulty === "MODERATE") return "badge bg-warning text-dark";
    return "badge bg-danger";
}

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
        const res = await api.get("/staff/treks");
        treks.value = res.data.treks;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load treks.";
    }
    finally {
        loading.value = false;
    }

}

onMounted(load);

</script>
