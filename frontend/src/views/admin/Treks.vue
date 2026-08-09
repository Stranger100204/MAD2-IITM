<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">

        <h2>Treks</h2>

        <button
            class="btn btn-success"
            data-bs-toggle="modal"
            data-bs-target="#trekModal"
        >
            + Add Trek
        </button>

    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading treks...</p>
    </div>

    <!-- Table -->
    <table v-else class="table table-bordered table-hover">

        <thead class="table-success">

            <tr>
                <th>Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Slots</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>

        </thead>

        <tbody>

            <tr
                v-for="trek in treks"
                :key="trek.id"
            >

                <td>{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td>
                    <span :class="difficultyBadge(trek.difficulty)">
                        {{ trek.difficulty }}
                    </span>
                </td>
                <td>{{ trek.duration_days }} days</td>
                <td>Available: {{ trek.available_slots }} / Total: {{ trek.total_slots }}</td>
                <td>
                    <span :class="statusBadge(trek.status)">
                        {{ trek.status }}
                    </span>
                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm me-2"
                        @click="editTrek(trek)"
                        data-bs-toggle="modal"
                        data-bs-target="#editTrekModal"
                    >
                        Edit
                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        @click="deleteTrek(trek)"
                        :disabled="deleting === trek.id"
                    >
                        <span v-if="deleting === trek.id">...</span>
                        <span v-else>Delete</span>
                    </button>

                </td>

            </tr>

            <tr v-if="treks.length === 0">

                <td colspan="7" class="text-center text-muted py-4">

                    No treks found.

                </td>

            </tr>

        </tbody>

    </table>

    <TrekModal @created="loadTreks" />

    <EditTrekModal
        :trek="selectedTrek"
        @updated="loadTreks"
    />

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";
import TrekModal from "../../components/admin/TrekModal.vue";
import EditTrekModal from "../../components/admin/EditTrekModal.vue";

const treks = ref([]);
const selectedTrek = ref(null);
const loading = ref(true);
const error = ref("");
const deleting = ref(null);

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

function editTrek(trek) {
    selectedTrek.value = { ...trek };
}

async function deleteTrek(trek) {

    if (!confirm(`Delete trek "${trek.name}"? This cannot be undone.`)) return;

    deleting.value = trek.id;

    try {

        await api.delete(`/admin/treks/${trek.id}`);

        await loadTreks();

    }

    catch (err) {

        error.value =
            err.response?.data?.error ||
            "Failed to delete trek.";

    }

    finally {

        deleting.value = null;

    }

}

async function loadTreks() {

    loading.value = true;
    error.value = "";

    try {

        const response = await api.get("/admin/treks");

        treks.value = response.data.treks;

    }

    catch (err) {

        error.value =
            err.response?.data?.error ||
            "Failed to load treks.";

    }

    finally {

        loading.value = false;

    }

}

onMounted(loadTreks);

</script>