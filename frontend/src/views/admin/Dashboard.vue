<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>



    <h2 class="mb-4">

        Welcome Admin

    </h2>

    <div class="row">

        <div class="col-md-3">

            <div class="card shadow-sm">

                <div class="card-body">

                    <h6>Total Treks</h6>

                    <h2>

                        {{ statistics.total_treks }}

                    </h2>

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card shadow-sm">

                <div class="card-body">

                    <h6>Total Users</h6>

                    <h2>

                        {{ statistics.total_users }}

                    </h2>

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card shadow-sm">

                <div class="card-body">

                    <h6>Total Staff</h6>

                    <h2>

                        {{ statistics.total_staff }}

                    </h2>

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card shadow-sm">

                <div class="card-body">

                    <h6>Total Bookings</h6>

                    <h2>

                        {{ statistics.total_bookings }}

                    </h2>

                </div>

            </div>

        </div>

    </div>

</Layout>

</template>

<script setup>

import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const statistics = ref({});

async function loadDashboard(){

    try{

        const response = await api.get("/admin/dashboard");

        statistics.value = response.data.statistics;

    }

    catch(err){

        console.log(err);

    }

}

onMounted(loadDashboard);

</script>