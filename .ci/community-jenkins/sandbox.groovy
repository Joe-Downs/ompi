// Hello World!


//def compilers = ["clang37", "clang38", "gcc5", "gcc6"]
//def platforms = ["ARMv8", "amazon_linux_1", "amazon_linux_2", "cray_cle",
//		 "rhel7", "rhel8", "sles_12", "ubuntu_16.04", "ubuntu_18.04"]

// JOE: Ignore cray_cle and Ubuntu 16
// ...possibly ignore others?  See which labels don't have
// corresponding VMs.  :-)

def make_the_stage(platform) {
    return {
        stage("this ${platform} stage") {
            node(platform) {
                println("We are in the stage on the ${platform} node")
                sh "hostname"
            }
        }
    }
}

def make_the_stages() {
    def platforms = ["rhel8", "amazon_linux_2"]
    def stage_map = [:]

    println("We have ${platforms} platforms")
    for (platform in platforms) {
        println("Running on the ${platform} platform")
        stage_map.put("this is ${platform} step", make_the_stage(platform))
    }

    def stage_list = []
    stage_list.add(stage_map)
    return stage_list
}

node('linux') {
    stage("Initialize") {
        println("Hello World!")
        sh "hostname"
        jms_stages = make_the_stages()
        println("Finished hello world")
    }

    parallelsAlwaysFailFast()
    for (s in jms_stages) {
        parallel(s)
    }

    stage("Finish") {
	println("It has ceased to be.")
    }
}
