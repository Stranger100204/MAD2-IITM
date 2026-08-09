<template>
  <div
    class="modal fade"
    id="editTrekModal"
    tabindex="-1"
  >
    <div class="modal-dialog modal-lg">

      <div class="modal-content">

        <div class="modal-header">

          <h5 class="modal-title">
            Edit Trek
          </h5>

          <button
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>

        </div>

        <div class="modal-body">

          <div v-if="error" class="alert alert-danger">{{ error }}</div>

          <div class="row">

            <div class="col-md-6 mb-3">
              <label>Name</label>
              <input
                v-model="trek.name"
                class="form-control"
              >
            </div>

            <div class="col-md-6 mb-3">
              <label>Location</label>
              <input
                v-model="trek.location"
                class="form-control"
              >
            </div>

            <div class="col-12 mb-3">
              <label>Description</label>
              <textarea
                v-model="trek.description"
                class="form-control"
              ></textarea>
            </div>

            <div class="col-md-4 mb-3">
              <label>Difficulty</label>
              <select
                v-model="trek.difficulty"
                class="form-select"
              >
                <option>EASY</option>
                <option>MODERATE</option>
                <option>HARD</option>
              </select>
            </div>

            <div class="col-md-4 mb-3">
              <label>Duration (days)</label>
              <input
                type="number"
                v-model.number="trek.duration_days"
                class="form-control"
              >
            </div>

            <div class="col-md-4 mb-3">
              <label>Total Slots</label>
              <input
                type="number"
                v-model.number="trek.total_slots"
                class="form-control"
              >
            </div>

            <div class="col-md-4 mb-3">
              <label>Status</label>
              <select v-model="trek.status" class="form-select">
                <option>PENDING</option>
                <option>APPROVED</option>
                <option>OPEN</option>
                <option>CLOSED</option>
                <option>COMPLETED</option>
              </select>
            </div>

            <div class="col-md-4 mb-3">
              <label>Start Date</label>
              <input
                type="date"
                v-model="trek.start_date"
                class="form-control"
              >
            </div>

            <div class="col-md-4 mb-3">
              <label>End Date</label>
              <input
                type="date"
                v-model="trek.end_date"
                class="form-control"
              >
            </div>

          </div>

        </div>

        <div class="modal-footer">

          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>

          <button
            class="btn btn-success"
            @click="updateTrek"
            :disabled="saving"
          >
            <span v-if="saving">Saving...</span>
            <span v-else>Update Trek</span>
          </button>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

import { reactive, ref, watch } from "vue";
import { Modal } from "bootstrap";
import api from "../../services/api";

const props = defineProps({
  trek: Object
});

const emit = defineEmits(["updated"]);

const saving = ref(false);
const error = ref("");

const trek = reactive({
  id: null,
  name: "",
  description: "",
  location: "",
  difficulty: "EASY",
  duration_days: 1,
  total_slots: 1,
  status: "OPEN",
  start_date: "",
  end_date: ""
});

watch(
  () => props.trek,
  (value) => {
    if (!value) return;
    error.value = "";
    Object.assign(trek, value);
  },
  { immediate: true }
);

async function updateTrek() {

  error.value = "";
  saving.value = true;

  try {

    await api.put(`/admin/treks/${trek.id}`, trek);

    const modalEl = document.getElementById("editTrekModal");
    Modal.getOrCreateInstance(modalEl).hide();

    setTimeout(() => {
      document.querySelectorAll(".modal-backdrop").forEach(el => el.remove());
      document.body.classList.remove("modal-open");
      document.body.style.removeProperty("overflow");
      document.body.style.removeProperty("padding-right");
    }, 300);

    emit("updated");

  }

  catch (err) {

    error.value =
      err.response?.data?.error ||
      "Failed to update trek.";

  }

  finally {

    saving.value = false;

  }

}

</script>
