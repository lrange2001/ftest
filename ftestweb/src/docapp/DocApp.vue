<template>
        <el-input
          v-model="query"
          placeholder="请输入文件名称"
          @input="onQueryChanged"
        />
        <el-tree-v2
          ref="treeRef"
          :data="data"
          :props="props"
          :filter-method="filterMethod"
          :height="208"
        />
</template>

<script>
    export default {
        name: "DocApp",
          data(){
              return {
            query: '',
            treeRef: '',
            data: [
                  {
                    value: '1',
                    label: 'Level one 1',
                    children: [
                      {
                        value: '1-1',
                        label: 'Level two 1-1',
                        children: [
                          {
                            value: '1-1-1',
                            label: 'Level three 1-1-1',
                          },
                        ],
                      },
                    ],
                  },
                  {
                    value: '2',
                    label: 'Level one 2',
                    children: [
                      {
                        value: '2-1',
                        label: 'Level two 2-1',
                        children: [
                          {
                            value: '2-1-1',
                            label: 'Level three 2-1-1',
                          },
                        ],
                      },
                      {
                        value: '2-2',
                        label: 'Level two 2-2',
                        children: [
                          {
                            value: '2-2-1',
                            label: 'Level three 2-2-1',
                          },
                        ],
                      },
                    ],
                  },
                ],
          props : {
            value: 'id',
            label: 'label',
            children: 'children',
          }
              }
          },
            methods: {

            }
    }
</script>

<style scoped>

</style>