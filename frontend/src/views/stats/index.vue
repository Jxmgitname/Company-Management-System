<template>
    <div class="app-container">
        <el-button type="primary" style="margin-bottom:12px" @click="fetchData">刷新</el-button>
        <el-row :gutter="16">
            <el-col :span="8">
                <el-card>员工总数<div style="font-size:28px">{{ stats.user_count }}</div></el-card>
            </el-col>
            <el-col :span="8">
                <el-card>岗位总数<div style="font-size:28px">{{ stats.role_count }}</div></el-card>
            </el-col>
            <el-col :span="8">
                <el-card>部门总数<div style="font-size:28px">{{ stats.dept_count }}</div></el-card>
            </el-col>
        </el-row>
        <el-row :gutter="16" style="margin-top:16px">
            <el-col :span="12">
                <el-card>
                部门人数
                <div ref="pieChart" style="height:320px"></div>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card>
                岗位人数
                <div ref="barChart" style="height:320px"></div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>

import { getDashboard } from '@/api/user'
import echarts from 'echarts'

export default {
  name: 'StatsOverview',
  data() {
    return {
        stats: {
            user_count: 0,
            role_count: 0,
            dept_count: 0,
            by_dept: [],
            by_role: []
        }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
   fetchData() {
      this.loading = true
      getDashboard().then(res => {
        this.stats = res.data
        this.$nextTick(() => { this.drawCharts() })
      }).catch(() => {
        this.loading = false
      })
    },
    drawCharts() {
        const pie = echarts.init(this.$refs.pieChart)
        pie.setOption({
            tooltip: { trigger: 'item' },
            series: [{ type: 'pie', data: this.stats.by_dept }]
        })
        const bar = echarts.init(this.$refs.barChart)
        const names = this.stats.by_role.map(item => item.name)
        const values = this.stats.by_role.map(item => item.value)
        bar.setOption({
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: names },
            yAxis: { type: 'value' },
            series: [{ type: 'bar', data: values }]
        })
    }
  }
}
</script>

