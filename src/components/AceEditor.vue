<template>
    <span class="float-end gear"  data-bs-toggle="dropdown" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-gear-fill" viewBox="0 0 16 16">
            <path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/>
        </svg>
    </span>
    <span class="float-end refresh" @click="refreshEditor">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
            <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"/>
            <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"/>
        </svg>
    </span>
    <ul class="dropdown-menu" style="min-width:290px" >
        <li class="dropdown-menu-item">
            <div class="row" data-stopPropagation="true">
                <div class="col-4">
                    <span class="dropdown-menu-item-title">界面风格: </span>
                </div>
                <div class="col-8 dropdown-menu-item-content">
                    <select v-model="skin" class="form-select dropdown-menu-item-select" aria-label="Default select" @change="changeEditSkin">
                        <option value="chrome">chrome</option>
                        <option value="monokai">monokai</option>
                    </select>
                </div>
            </div>
        </li>
        <li class="dropdown-menu-item">
            <div class="row" data-stopPropagation="true">
                <div class="col-4">
                    <span class="dropdown-menu-item-title">编辑类型: </span>
                </div>
                <div class="col-8 dropdown-menu-item-content">
                    <select class="form-select dropdown-menu-item-select" aria-label="Default select" v-model="editor_mode" @change="changeEditMode">
                        <option value="vscode">Standard</option>
                        <option value="vim">Vim</option>
                        <option value="emacs">Emacs</option>
                    </select>
                </div>
            </div>
        </li>
        <li class="dropdown-menu-item">
            <div class="row" data-stopPropagation="true">
                <div class="col-4">
                    <span class="dropdown-menu-item-title">缩进长度: </span>
                </div>
                <div class="col-8 dropdown-menu-item-content">
                    <select class="form-select dropdown-menu-item-select" aria-label="Default select" v-model="editor_space" @change="changeEditorSpace">
                        <option value="2">2个空格</option>
                        <option value="4">4个空格</option>
                        <option value="8">8个空格</option>
                    </select>
                </div>
            </div>
        </li>
        <li class="dropdown-menu-item">
            <div class="row" data-stopPropagation="true">
                <div class="col-4">
                    <span class="dropdown-menu-item-title">字号: </span>
                </div>
                <div class="col-8">
                    <el-input-number
                        v-model="fontsize"
                        :min="5"
                        :max="60"
                        size="small"
                        controls-position="right"
                        @change="changeEditFont" />
                </div>
            </div>
        </li>
      </ul>
    <VAceEditor
        :id="'codeEditor' + flag"
        @init="editorInit"
        style="height: 300px" />
</template>

<script>
import { VAceEditor } from 'vue3-ace-editor';
import * as ace from 'ace-builds';
import $ from 'jquery';
import { ref } from 'vue';

export default {
    name: 'AceEditor',
    components: {
        VAceEditor,
    },
    setup(props, context) {
        ace.config.set(
            "basePath", 
            "https://cdn.jsdelivr.net/npm/ace-builds@" + require('ace-builds').version + "/src-noconflict/");


        let editor = null;
        let skin = ref('chrome');
        let fontsize = ref(11);
        let editor_mode = ref('vscode');
        let editor_space = ref(4);
        let flag = ref('');

        const editorInit = (editor) => {
            editor.renderer.setShowPrintMargin(false);
        }

        // 使dropdown点击不会消失
        //指定要操作的元素的click事件停止传播—定义属性值data-stopPropagation的元素点击时停止传播事件
        $("body").on('click','[data-stopPropagation]',function (e) {
            e.stopPropagation();
        });
        const initModal = (t, val) => {
            flag.value = t;
            editor = ace.edit('codeEditor' + flag.value);

            if(localStorage.getItem("editor_skin") !== null) {
                skin.value = localStorage.getItem("editor_skin");
            }

            if(localStorage.getItem("editor_fontsize") !== null) {
                fontsize.value = parseInt(localStorage.getItem("editor_fontsize"));
            }

            if(localStorage.getItem("editor_mode") !== null) {
                editor_mode.value = localStorage.getItem("editor_mode");
            }

            if(localStorage.getItem("editor_space") !== null) {
                editor_space.value = localStorage.getItem("editor_space")
            }

            editor.setOptions({
                'fontSize': `${fontsize.value}pt`,
                'tabSize': parseInt(editor_space.value),
            });
            editor.setKeyboardHandler("ace/keyboard/" + editor_mode.value);
            editor.setTheme("ace/theme/" + skin.value);
            editor.setValue(val);

            editor.getSession().on('change', () => {
                context.emit('updateBotContent', editor.getValue());
            });
        }

        const changeEditSkin = () => {
            editor.setTheme("ace/theme/" + skin.value);
            localStorage.setItem("editor_skin", skin.value);
        }

        const changeEditFont = num => {
            editor.setOptions({
                'fontSize': `${num}pt`,
            })
            localStorage.setItem("editor_fontsize", num);
        }

        const changeEditMode = () => {
            editor.setKeyboardHandler("ace/keyboard/" + editor_mode.value);
            localStorage.setItem("editor_mode", editor_mode.value);
        }

        const changeEditorSpace = () => {
            editor.setOptions({
                'tabSize': parseInt(editor_space.value),
            })
            localStorage.setItem("editor_space", editor_space.value);
        }

        const refreshEditor = () => {
            editor.setValue("");
        }

        return {
            editorInit,
            initModal,
            changeEditSkin,
            changeEditFont,
            changeEditMode,
            changeEditorSpace,
            skin,
            fontsize,
            editor_mode,
            editor_space,
            refreshEditor,
            flag,
        }
    }
}
</script>

<style scoped>
.refresh {
    margin-right: 15px;
    cursor: pointer;
}

.refresh:hover {
    transform: scale(1.2);
    transition: 100ms;
}

.gear {
    cursor: pointer;
    margin-right: 15px;
}

.gear:hover {
    transform: scale(1.2);
    transition: 100ms;
}

.dropdown-menu-item {
    margin-top: 10px;
}

.dropdown-menu-item-title {
    margin-left: 10px;
}

.dropdown-menu-item-select {
    height: 35px;
    width: 140px;
    margin-right: 10px;
}
</style>