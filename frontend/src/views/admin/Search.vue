<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">Search</h2>

    <!-- Search bar -->
    <div class="input-group mb-4">
        <input
            v-model="query"
            class="form-control form-control-lg"
            placeholder="Search users, staff, or treks..."
            @keyup.enter="search"
        >
        <button class="btn btn-success" @click="search" :disabled="searching">
            <span v-if="searching">Searching...</span>
            <span v-else>Search</span>
        </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Results -->
    <div v-if="searched">

        <!-- Users -->
        <div class="mb-4">
            <h5>👥 Users ({{ results.users?.length || 0 }})</h5>
            <table class="table table-bordered table-sm">
                <thead class="table-light">
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="u in results.users" :key="u.id">
                        <td>{{ u.name }}</td>
                        <td>{{ u.email }}</td>
                        <td><span class="badge bg-secondary">{{ u.role }}</span></td>
                        <td>
                            <span :class="u.status === 'ACTIVE' ? 'badge bg-success' : 'badge bg-danger'">
                                {{ u.status }}
                            </span>
                        </td>
                    </tr>
                    <tr v-if="!results.users?.length">
                        <td colspan="4" class="text-center text-muted">No users found.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Staff -->
        <div class="mb-4">
            <h5>👷 Staff ({{ results.staff?.length || 0 }})</h5>
            <table class="table table-bordered table-sm">
                <thead class="table-light">
                    <tr>
                        <th>Name</th>
                        <th>Specialization</th>
                        <th>Experience</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="s in results.staff" :key="s.id">
                        <td>{{ s.user?.name }}</td>
                        <td>{{ s.specialization }}</td>
                        <td>{{ s.experience_years }} yrs</td>
                    </tr>
                    <tr v-if="!results.staff?.length">
                        <td colspan="3" class="text-center text-muted">No staff found.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Treks -->
        <div class="mb-4">
            <h5>🏔 Treks ({{ results.treks?.length || 0 }})</h5>
            <table class="table table-bordered table-sm">
                <thead class="table-light">
                    <tr>
                        <th>Name</th>
                        <th>Location</th>
                        <th>Difficulty</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="t in results.treks" :key="t.id">
                        <td>{{ t.name }}</td>
                        <td>{{ t.location }}</td>
                        <td>{{ t.difficulty }}</td>
                        <td><span class="badge bg-secondary">{{ t.status }}</span></td>
                    </tr>
                    <tr v-if="!results.treks?.length">
                        <td colspan="4" class="text-center text-muted">No treks found.</td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>

    <!-- Initial state -->
    <div v-if="!searched && !searching" class="text-center text-muted py-5">
        <p>Enter a search term above to find users, staff, or treks.</p>
    </div>

</Layout>

</template>

<script setup>

import { ref, reactive } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const query = ref("");
const results = reactive({ users: [], staff: [], treks: [] });
const searching = ref(false);
const searched = ref(false);
const error = ref("");

async function search() {

    if (!query.value.trim()) return;

    searching.value = true;
    searched.value = false;
    error.value = "";

    try {
        const res = await api.get("/admin/search", {
            params: { q: query.value.trim() }
        });

        results.users = res.data.users || [];
        results.staff = res.data.staff || [];
        results.treks = res.data.treks || [];
        searched.value = true;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Search failed.";
    }
    finally {
        searching.value = false;
    }

}

</script>
