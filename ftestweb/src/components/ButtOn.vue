<template>
  <div class="container">
      <a class="button">
          <div class="button__line"></div>
          <div class="button__line"></div>
          <span class="button__text" @click="loginclick">{{ buttonmsg }}</span>
      </a>
  </div>

    
</template>

<script>
    export default {
        name: "ButtOn",
        props: {
            buttonmsg: String
        }
    }
</script>

<style scoped>
.button {
	position:relative;
	z-index:0;
	width:200px;
	height: 34px;
	text-decoration:none;
	font-size:14px;
	font-weight:bold;
	color:var(--line_color);
	letter-spacing:2px;
	transition:all .3s ease;
}
.button__text {
	display:flex;
	justify-content:center;
	align-items:center;
	width:100%;
	height:100%;
}
.button::before,.button::after,.button__text::before,.button__text::after {
	content:'';
	position:absolute;
	height:3px;
	border-radius:1px;
	background:var(--line_color);
	transition:all .5s ease;
}
.button::before {
	top:0;
	left:54px;
	width:calc( 100% - 56px * 2 - 16px );
}
.button::after {
	top:0;
	right:54px;
	width:8px;
}
.button__text::before {
	bottom:0;
	right:54px;
	width:calc( 100% - 56px * 2 - 16px );
}
.button__text::after {
	bottom:0;
	left:54px;
	width:8px;
}
.button__line {
	position:absolute;
	top:0;
	width:56px;
	height:100%;
	overflow:hidden;
}
.button__line::before {
	content:'';
	position:absolute;
	top:0;
	width:150%;
	height:100%;
	box-sizing:border-box;
	border-radius: 6px;
	border:solid 3px var(--line_color);
}
.button__line:nth-child(1),.button__line:nth-child(1)::before {
	left:0;
}
.button__line:nth-child(2),.button__line:nth-child(2)::before {
	right:0;
}
.button:hover {
	letter-spacing:6px;
}
.button:hover::before,.button:hover .button__text::before {
	width:8px;
}
.button:hover::after,.button:hover .button__text::after {
	width:calc( 100% - 56px * 2 - 16px );
}

@keyframes drow1 {
	0% {
	height:0;
}
100% {
	height:100px;
}
}@keyframes drow2 {
	0% {
	width:0;
	opacity:0;
}
10% {
	opacity:0;
}
11% {
	opacity:1;
}
100% {
	width:120px;
}
}@keyframes drow3 {
	0% {
	width:0;
}
100% {
	width:80px;
}
}@keyframes drow4 {
	0% {
	height:0;
}
100% {
	height:120px;
}
}@keyframes drow5 {
	0% {
	width:0;
}
100% {
	width:124px;
}
}
.container {
    --line_color:#555555;
	--back_color:#FFECF6;
    padding-top: 10px;
	display:flex;
	flex-direction:column;
	justify-content:center;
	align-items:center;
}

</style>