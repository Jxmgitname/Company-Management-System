<template>
  <div class="company-login">
    <header class="company-header">
      <div class="company-header-inner">
        <div class="brand">
          <span class="brand-mark" />
          <span class="brand-name">公司内部后台管理系统</span>
          <span class="brand-split" />
          <span class="brand-sub">内部办公</span>
        </div>
      </div>
    </header>

    <main class="company-main">
      <section class="panel">
        <div class="login-card">
          <h2 class="login-title">账号登录</h2>

          <el-form
            ref="loginForm"
            :model="loginForm"
            :rules="loginRules"
            class="company-form"
            autocomplete="on"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="账号名"
                prefix-icon="el-icon-user"
                tabindex="1"
                @keyup.enter.native="handleLogin"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                :type="passwordType"
                placeholder="登录密码"
                prefix-icon="el-icon-lock"
                tabindex="2"
                @keyup.enter.native="handleLogin"
              >
                <i
                  slot="suffix"
                  class="el-input__icon el-icon-view password-eye"
                  @click="showPwd"
                />
              </el-input>
            </el-form-item>
            <el-button
              class="submit-btn"
              type="primary"
              :loading="loading"
              @click.native.prevent="handleLogin"
            >
              登录
            </el-button>
          </el-form>
        </div>
      </section>
    </main>

    <footer class="company-footer">
      <p>© 2015-2026 公司内部后台管理系统 版权所有 ICP备00000000号-1</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value || !value.trim()) {
        callback(new Error('请输入账号名'))
      } else if (value.trim().length < 3) {
        callback(new Error('账号名不少于 3 位'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码不能少于 6 位'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: 'admin1',
        password: '123456'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password'
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/login', this.loginForm).then(() => {
          this.$router.push({ path: '/stats/overview' })
          this.loading = false
        }).catch(() => {
          this.loading = false
        })
      })
    }
  }
}
</script>

<style lang="scss">
.company-login {
  .el-input__inner {
    height: 40px;
    line-height: 40px;
    border-radius: 0;
    border-color: #d9d9d9;
  }

  .el-input__inner:focus {
    border-color: #3b82f6;
  }

  .el-form-item {
    margin-bottom: 18px;
  }

  .el-button--primary {
    background: #3b82f6;
    border-color: #3b82f6;
    border-radius: 0;
    height: 40px;
    font-size: 16px;
    letter-spacing: 4px;
  }

  .el-button--primary:hover,
  .el-button--primary:focus {
    background: #3b82f6;
    border-color: #3b82f6;
  }
}
</style>

<style lang="scss" scoped>
$orange: #3b82f6;

.company-login {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(rgba(247, 248, 250, .55), rgba(247, 248, 250, .55)),
    url('~@/assets/login-bg.jpg') no-repeat center center;
  background-size: cover;
  display: flex;
  flex-direction: column;
}



.company-header,
.company-main,
.company-footer {
  position: relative;
  z-index: 1;
}

.company-header {
  height: 50px;
  background: transparent;
}

.company-header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  color: #111;
}

.brand-mark {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  background: $orange;
  clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
}

.brand-split {
  width: 1px;
  height: 16px;
  background: #ddd;
  margin: 0 12px;
}

.brand-sub {
  font-size: 14px;
  color: #666;
}

.company-main {
  flex: 1;
  width: 100%;
  padding: 32px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel {
  width: 400px;
  flex-shrink: 0;
}

.login-card {
  width: 100%;
  background: #fff;
  padding: 28px 32px 32px;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(80, 90, 140, .12);
}

.login-title {
  margin: 0 0 28px;
  font-size: 20px;
  font-weight: 600;
  color: #111;
  text-align: center;
}

.submit-btn {
  width: 100%;
  margin-top: 6px;
}

.tips {
  margin: 16px 0 0;
  font-size: 12px;
  color: #999;
  line-height: 1.6;
}

.password-eye {
  cursor: pointer;
  color: #c0c4cc;
}

.company-footer {
  padding: 16px 24px 24px;
  text-align: center;
  color: #8a8fa3;
  font-size: 12px;
}

@media (max-width: 960px) {
  .company-main {
    padding-top: 24px;
  }

  .panel,
  .login-card {
    width: 100%;
    max-width: 400px;
  }
}
</style>
