<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Staff Management</h2>
        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addStaffModal">
            + Add Staff
        </button>
    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="success" class="alert alert-success alert-dismissible">
        {{ success }}
        <button type="button" class="btn-close" @click="success = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading staff...</p>
    </div>

    <!-- Assign Staff to Trek -->
    <div class="card mb-4">
        <div class="card-header fw-bold">Assign Staff to Trek</div>
        <div class="card-body">
            <div class="row g-2 align-items-end">
                <div class="col-md-5">
                    <label class="form-label">Select Trek</label>
                    <select v-model="assignForm.trek_id" class="form-select">
                        <option value="">-- Select Trek --</option>
                        <option v-for="t in treks" :key="t.id" :value="t.id">{{ t.name }}</option>
                    </select>
                </div>
                <div class="col-md-5">
                    <label class="form-label">Select Staff</label>
                    <select v-model="assignForm.staff_id" class="form-select">
                        <option value="">-- Select Staff --</option>
                        <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.user?.name }}</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button
                        class="btn btn-primary w-100"
                        @click="assignStaff"
                        :disabled="assigning || !assignForm.trek_id || !assignForm.staff_id"
                    >
                        <span v-if="assigning">...</span>
                        <span v-else>Assign</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Staff Table -->
    <table v-if="!loading" class="table table-bordered table-hover">

        <thead class="table-success">
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Specialization</th>
                <th>Experience</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            <tr v-for="member in staffList" :key="member.id">
                <td>{{ member.id }}</td>
                <td>{{ member.user?.name }}</td>
                <td>{{ member.user?.email }}</td>
                <td>{{ member.user?.phone || '—' }}</td>
                <td>{{ member.specialization }}</td>
                <td>{{ member.experience_years }} yrs</td>
                <td>
                    <span :class="member.user?.status === 'ACTIVE' ? 'badge bg-success' : 'badge bg-danger'">
                        {{ member.user?.status }}
                    </span>
                </td>
                <td>
                    <button
                        class="btn btn-warning btn-sm me-1"
                        @click="openEdit(member)"
                        data-bs-toggle="modal"
                        data-bs-target="#editStaffModal"
                    >Edit</button>
                    <button
                        class="btn btn-danger btn-sm"
                        @click="deleteStaff(member)"
                        :disabled="deleting === member.id"
                    >
                        <span v-if="deleting === member.id">...</span>
                        <span v-else>Remove</span>
                    </button>
                </td>
            </tr>

            <tr v-if="staffList.length === 0">
                <td colspan="8" class="text-center text-muted py-4">No staff found.</td>
            </tr>

        </tbody>

    </table>

    <!-- Add Staff Modal -->
    <div class="modal fade" id="addStaffModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Add Staff Member</h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div v-if="addError" class="alert alert-danger">{{ addError }}</div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Name <span class="text-danger">*</span></label>
                            <input v-model="addForm.name" class="form-control" placeholder="Full name">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Email <span class="text-danger">*</span></label>
                            <input v-model="addForm.email" type="email" class="form-control" placeholder="Email">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Password <span class="text-danger">*</span></label>
                            <input v-model="addForm.password" type="password" class="form-control" placeholder="Password">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Phone <span class="text-danger">*</span></label>
                            <input v-model="addForm.phone" class="form-control" placeholder="Phone number">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Specialization <span class="text-danger">*</span></label>
                            <input v-model="addForm.specialization" class="form-control" placeholder="e.g. Mountain Trekking">
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Experience (years) <span class="text-danger">*</span></label>
                            <input v-model="addForm.experience_years" type="number" min="0" class="form-control">
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Emergency Contact <span class="text-danger">*</span></label>
                            <input v-model="addForm.emergency_contact" class="form-control" placeholder="Emergency phone">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button class="btn btn-success" @click="createStaff" :disabled="addSaving">
                        <span v-if="addSaving">Saving...</span>
                        <span v-else>Create Staff</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit Staff Modal -->
    <div class="modal fade" id="editStaffModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Staff Member</h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div v-if="editError" class="alert alert-danger">{{ editError }}</div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Name</label>
                            <input v-model="editForm.name" class="form-control">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Phone</label>
                            <input v-model="editForm.phone" class="form-control">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Specialization</label>
                            <input v-model="editForm.specialization" class="form-control">
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Experience (years)</label>
                            <input v-model="editForm.experience_years" type="number" min="0" class="form-control">
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Emergency Contact</label>
                            <input v-model="editForm.emergency_contact" class="form-control">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button class="btn btn-success" @click="updateStaff" :disabled="editSaving">
                        <span v-if="editSaving">Saving...</span>
                        <span v-else>Update Staff</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

</Layout>

</template>

<script setup>

import { ref, reactive, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { Modal } from "bootstrap";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const staffList = ref([]);
const treks = ref([]);
const loading = ref(true);
const error = ref("");
const success = ref("");
const deleting = ref(null);
const assigning = ref(false);

// Add form
const addForm = reactive({
    name: "", email: "", password: "", phone: "",
    specialization: "", experience_years: 1, emergency_contact: ""
});
const addSaving = ref(false);
const addError = ref("");

// Edit form
const editForm = reactive({
    id: null, name: "", phone: "",
    specialization: "", experience_years: 1, emergency_contact: ""
});
const editSaving = ref(false);
const editError = ref("");

// Assign form
const assignForm = reactive({ trek_id: "", staff_id: "" });

async function loadStaff() {

    loading.value = true;

    try {
        const res = await api.get("/admin/staff");
        staffList.value = res.data.staff;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load staff.";
    }
    finally {
        loading.value = false;
    }

}

async function loadTreks() {

    try {
        const res = await api.get("/admin/treks");
        treks.value = res.data.treks;
    }
    catch { /* silent */ }

}

async function createStaff() {

    addError.value = "";
    addSaving.value = true;

    try {
        await api.post("/admin/staff", addForm);

        Modal.getInstance(document.getElementById("addStaffModal"))?.hide();

        // Reset form
        Object.assign(addForm, {
            name: "", email: "", password: "", phone: "",
            specialization: "", experience_years: 1, emergency_contact: ""
        });

        success.value = "Staff member created successfully.";
        await loadStaff();
    }
    catch (err) {
        addError.value = err.response?.data?.error || "Failed to create staff.";
    }
    finally {
        addSaving.value = false;
    }

}

function openEdit(member) {

    editError.value = "";
    editForm.id = member.id;
    editForm.name = member.user?.name || "";
    editForm.phone = member.user?.phone || "";
    editForm.specialization = member.specialization || "";
    editForm.experience_years = member.experience_years || 0;
    editForm.emergency_contact = member.emergency_contact || "";

}

async function updateStaff() {

    editError.value = "";
    editSaving.value = true;

    try {
        await api.put(`/admin/staff/${editForm.id}`, {
            name: editForm.name,
            phone: editForm.phone,
            specialization: editForm.specialization,
            experience_years: editForm.experience_years,
            emergency_contact: editForm.emergency_contact
        });

        Modal.getInstance(document.getElementById("editStaffModal"))?.hide();

        success.value = "Staff member updated successfully.";
        await loadStaff();
    }
    catch (err) {
        editError.value = err.response?.data?.error || "Failed to update staff.";
    }
    finally {
        editSaving.value = false;
    }

}

async function deleteStaff(member) {

    if (!confirm(`Remove staff member "${member.user?.name}"?`)) return;

    deleting.value = member.id;

    try {
        await api.delete(`/admin/staff/${member.id}`);
        success.value = "Staff member removed successfully.";
        await loadStaff();
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to remove staff.";
    }
    finally {
        deleting.value = null;
    }

}

async function assignStaff() {

    assigning.value = true;

    try {
        await api.put(`/admin/treks/${assignForm.trek_id}/assign`, {
            staff_id: assignForm.staff_id
        });

        success.value = "Staff assigned to trek successfully.";
        assignForm.trek_id = "";
        assignForm.staff_id = "";
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to assign staff.";
    }
    finally {
        assigning.value = false;
    }

}

onMounted(async () => {
    await Promise.all([loadStaff(), loadTreks()]);
});

</script>
