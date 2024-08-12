<template>
  <div class="app-container">
    <div class="app-container-inner">
      <div class="wscn-http403-container ">
        <div class="bullshit__oops view_mobile"><span>&#127881; 欢迎您</span>
          <div> {{ name }}</div>
          <div class="success_tips_txt">
            进入<span>{{ workspace_name }}</span>
            的数字员工空间
          </div>
        </div>
        <div class="wscn-http403">
          <div class="pic-403">
            <img class="pic-403__parent" src="@/assets/success/success.png" alt="403" />
            <img class="pic-403__child left" src="@/assets/403_images/403_cloud.png" alt="403" />
            <img class="pic-403__child mid" src="@/assets/403_images/403_cloud.png" alt="403" />
            <img class="pic-403__child right" src="@/assets/403_images/403_cloud.png" alt="403" />
          </div>
        </div>
        <div class="button-box">
          <div class="bullshit__oops view_pc"><span>&#127881; 欢迎 {{ name }}</span>
            <div class="success_tips_txt">
              进入<span>{{ workspace_name }}</span>
              <div>的数字员工空间</div>
            </div>
          </div>
          <div class="bullshit">
            <el-button class="button-ai" type="primary" size="large" @click="goToAI">立即体验</el-button>

            <el-button class="button-admin" size="large" @click="$router.push('/workspace')"
              v-if="roleTypes != 'normal' && platform == 'pc'">进入管理后台</el-button>
          </div>
          <div v-if="roleTypes != 'normal'" class="tips_pc">
            <div>打造数字员工请在PC端访问</div>
            <div>{{ websiteUrl }}</div>
          </div>
        </div>
        <div class="view_pc">

        </div>
      </div>

    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { getQueryObject } from "@/utils/index"
const urlQuery = getQueryObject(null)
const websiteUrl = import.meta.env.VITE_APP_WEBSITE ? import.meta.env.VITE_APP_WEBSITE : window.globalVariable.WEBSITE
const { roleTypes, workspace_name, name } = urlQuery
const goToAI = () => {
  const uri = import.meta.env.VITE_APP_DIFY_URL ? import.meta.env.VITE_APP_DIFY_URL : window.globalVariable.DIFY_URL
  console.log(`${uri}?console_token=${localStorage.token}`)
  window.open(`${uri}?console_token=${localStorage.token}`, '_blank')
}
import { useUserStore } from '@/store/modules/user'
const platform = ref("")
function isPlatform() {
  var ua = navigator.userAgent.toLowerCase();
  if (ua.match(/MicroMessenger/i) == "micromessenger") {
    platform.value = "wechat"
  } else {
    platform.value = "pc"
  }
}
onMounted(() => {
  isPlatform()
})

</script>

<style lang="scss" scoped>
.tips_pc {
  background: rgba(184, 184, 184, .23);
  padding: 10px;
  margin-top: 10px;
  width: 250px;
}

.wscn-http403-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
}

.view_pc {
  display: block;
}

.view_mobile {
  display: none;
}

a {
  text-decoration: none;
}

.wscn-http403 {
  position: relative;
  width: 1200px;
  display: flex;
  justify-content: center;
  align-items: center;

  overflow: hidden;
  flex: 10;

  .pic-403 {
    position: relative;
    float: left;
    width: 600px;
    overflow: hidden;

    &__parent {
      width: 100%;
    }

    &__child {
      position: absolute;

      &.left {
        width: 80px;
        top: 17px;
        left: 220px;
        opacity: 0;
        animation-name: cloudLeft;
        animation-duration: 2s;
        animation-timing-function: linear;
        animation-fill-mode: forwards;
        animation-delay: 1s;
      }

      &.mid {
        width: 46px;
        top: 10px;
        left: 420px;
        opacity: 0;
        animation-name: cloudMid;
        animation-duration: 2s;
        animation-timing-function: linear;
        animation-fill-mode: forwards;
        animation-delay: 1.2s;
      }

      &.right {
        width: 62px;
        top: 100px;
        left: 500px;
        opacity: 0;
        animation-name: cloudRight;
        animation-duration: 2s;
        animation-timing-function: linear;
        animation-fill-mode: forwards;
        animation-delay: 1s;
      }

      @keyframes cloudLeft {
        0% {
          top: 17px;
          left: 220px;
          opacity: 0;
        }

        20% {
          top: 33px;
          left: 188px;
          opacity: 1;
        }

        80% {
          top: 81px;
          left: 92px;
          opacity: 1;
        }

        100% {
          top: 97px;
          left: 60px;
          opacity: 0;
        }
      }

      @keyframes cloudMid {
        0% {
          top: 10px;
          left: 420px;
          opacity: 0;
        }

        20% {
          top: 40px;
          left: 360px;
          opacity: 1;
        }

        70% {
          top: 130px;
          left: 180px;
          opacity: 1;
        }

        100% {
          top: 160px;
          left: 120px;
          opacity: 0;
        }
      }

      @keyframes cloudRight {
        0% {
          top: 100px;
          left: 500px;
          opacity: 0;
        }

        20% {
          top: 120px;
          left: 460px;
          opacity: 1;
        }

        80% {
          top: 180px;
          left: 340px;
          opacity: 1;
        }

        100% {
          top: 200px;
          left: 300px;
          opacity: 0;
        }
      }
    }
  }

  .bullshit {
    position: relative;
    float: left;
    width: 300px;
    padding: 30px 0;
    overflow: hidden;

    &__oops {
      font-size: 32px;
      font-weight: bold;
      line-height: 40px;
      color: #1482f0;
      opacity: 0;
      margin-bottom: 20px;
      animation-name: slideUp;
      animation-duration: 0.5s;
      animation-fill-mode: forwards;
    }

    &__headline {
      font-size: 20px;
      line-height: 24px;
      color: #222;
      font-weight: bold;
      opacity: 0;
      margin-bottom: 10px;
      animation-name: slideUp;
      animation-duration: 0.5s;
      animation-delay: 0.1s;
      animation-fill-mode: forwards;
    }

    &__info {
      font-size: 13px;
      line-height: 21px;
      color: grey;
      opacity: 0;
      margin-bottom: 30px;
      animation-name: slideUp;
      animation-duration: 0.5s;
      animation-delay: 0.2s;
      animation-fill-mode: forwards;
    }

    &__return-home {
      display: block;
      float: left;
      width: 110px;
      height: 36px;
      background: #1482f0;
      border-radius: 100px;
      text-align: center;
      color: #ffffff;
      opacity: 0;
      font-size: 14px;
      line-height: 36px;
      cursor: pointer;
      animation-name: slideUp;
      animation-duration: 0.5s;
      animation-delay: 0.3s;
      animation-fill-mode: forwards;
    }

    @keyframes slideUp {
      0% {
        transform: translateY(60px);
        opacity: 0;
      }

      100% {
        transform: translateY(0);
        opacity: 1;
      }
    }
  }
}

.bullshit__oops {
  font-size: 22px;
  font-weight: 800;
  color: #3999f8;
  text-align: center;
}

.bullshit__oops span {
  font-size: 24px;
  margin: 0 2px;
  color: #1482f0
}

.button-box {
  flex: 5;
  text-align: left;

  .bullshit__oops {
    text-align: left;
    margin-bottom: 20px;

  }
}






@media screen and (max-width: 768px) {
  .button-box {
    flex: 0
  }

  .view_mobile {
    display: block;
  }

  .view_pc {
    display: none;
  }

  .wscn-http403-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
  }

  .success_tips_txt {
    display: table;
    text-align: left;
    margin: auto;
    margin-top: 100px;
    margin-bottom: 20px;
    font-size: 26px;

  }




  .bullshit__oops {
    font-size: 20px;
  }

  .bullshit__oops span {
    font-size: 24px;
  }

  .bullshit {
    padding-top: 100px;
    text-align: center;
    margin-bottom: 20px;
  }

  .wscn-http403 {
    display: none;
  }

  .wscn-http403 {
    width: 100%;
    padding: 0px;
    margin: 0px
  }


  .success_tips_txt {
    font-size: 18px;
  }

  .success_tips_txt span {
    font-size: 18px;
  }


  .button-admin {
    display: none;
  }

  .button-ai {
    width: 300px;
    height: 70px;
    font-size: 26px;
  }
}
</style>
