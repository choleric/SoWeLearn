module.exports = function(grunt){
  grunt.initConfig({
    pkg : grunt.file.readJSON('package.json'),
    less : {
		compile:{
		  options:{},
		  files:{
		    '../css/left.css':'../css/less/left.less',
		    '../css/reset.css':'../css/less/reset.less',
		    '../css/right.css':'../css/less/right.less',
		    '../css/tooltip.css':'../css/less/tooltip.less',
		    '../css/mainless.css':'../css/less/main.less',
		  }
		}
    },
    watch: {
		less:{
		  files: '../css/less/*.less',
		  tasks: ['less']
		}
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default',['less','watch']);
}
