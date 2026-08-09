<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Reports &amp; Statistics</h2>
        <div class="d-flex gap-2">
            <button
                class="btn btn-outline-success"
                @click="generateReport"
                :disabled="generating"
            >
                <span v-if="generating">Generating...</span>
                <span v-else>📊 Generate Report</span>
            </button>
            <button
                v-if="reportReady"
                class="btn btn-success"
                @click="viewReport"
            >
                👁 View Report
            </button>
        </div>
    </div>

    <!-- Alerts -->
    <div v-if="reportMsg" class="alert alert-success alert-dismissible">
        {{ reportMsg }}
        <button class="btn-close" @click="reportMsg = ''"></button>
    </div>
    <div v-if="reportError" class="alert alert-danger alert-dismissible">
        {{ reportError }}
        <button class="btn-close" @click="reportError = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading reports...</p>
    </div>

    <div v-if="!loading">

        <!-- Stats cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body text-center">
                        <div class="fs-2">🏔</div>
                        <h6 class="text-muted">Total Treks</h6>
                        <h2>{{ statistics.total_treks }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body text-center">
                        <div class="fs-2">👥</div>
                        <h6 class="text-muted">Total Users</h6>
                        <h2>{{ statistics.total_users }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body text-center">
                        <div class="fs-2">👷</div>
                        <h6 class="text-muted">Total Staff</h6>
                        <h2>{{ statistics.total_staff }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body text-center">
                        <div class="fs-2">📋</div>
                        <h6 class="text-muted">Total Bookings</h6>
                        <h2>{{ statistics.total_bookings }}</h2>
                    </div>
                </div>
            </div>
        </div>

        <!-- Completed Trek History -->
        <h5 class="mb-3">Completed Trek History</h5>

        <div v-if="historyError" class="alert alert-danger">{{ historyError }}</div>

        <table class="table table-bordered table-hover">

            <thead class="table-success">
                <tr>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Total Slots</th>
                    <th>Participants</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="trek in history" :key="trek.id">
                    <td>{{ trek.name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>
                        <span :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span>
                    </td>
                    <td>{{ trek.duration_days }} days</td>
                    <td>{{ trek.total_slots }}</td>
                    <td>{{ trek.total_slots - trek.available_slots }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>{{ trek.end_date }}</td>
                </tr>

                <tr v-if="history.length === 0">
                    <td colspan="8" class="text-center text-muted py-4">No completed treks found.</td>
                </tr>

            </tbody>

        </table>

    </div>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const statistics = ref({});
const history = ref([]);
const loading = ref(true);
const historyError = ref("");
const generating = ref(false);
const reportReady = ref(false);
const reportMsg = ref("");
const reportError = ref("");

function difficultyBadge(difficulty) {
    if (difficulty === "EASY") return "badge bg-success";
    if (difficulty === "MODERATE") return "badge bg-warning text-dark";
    return "badge bg-danger";
}

async function load() {

    loading.value = true;

    try {
        const [dashRes, histRes] = await Promise.all([
            api.get("/admin/dashboard"),
            api.get("/admin/history")
        ]);

        statistics.value = dashRes.data.statistics;
        history.value = histRes.data.history;
    }
    catch (err) {
        historyError.value = err.response?.data?.error || "Failed to load reports.";
    }
    finally {
        loading.value = false;
    }

}

async function generateReport() {

    generating.value = true;
    reportMsg.value = "";
    reportError.value = "";
    reportReady.value = false;

    try {
        await api.post("/admin/report/generate");
        reportMsg.value = "Report generated! Click 'View Report' to open it.";
        reportReady.value = true;
    }
    catch (err) {
        reportError.value = err.response?.data?.error || "Failed to generate report.";
    }
    finally {
        generating.value = false;
    }

}

function viewReport() {
    const token = localStorage.getItem("token");
    const t = new Date().getTime(); // Cache busting
    fetch(`http://localhost:5000/api/admin/report/download?t=${t}`, {
        headers: { "Authorization": `Bearer ${token}` }
    })
    .then(res => {
        if (!res.ok) throw new Error("Not found");
        return res.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        window.open(url, "_blank");
    })
    .catch(() => {
        reportError.value = "Report not found. Please generate it first.";
    });
}

onMounted(load);

</script>
