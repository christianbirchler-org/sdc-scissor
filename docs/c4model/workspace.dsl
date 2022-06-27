workspace {
    model {
        user = person "User"
        sdcScissor = softwareSystem "SDC-Scissor" {
            python = container "Python" {
                cli = component "CLI"
                simulatorAPI = component "Simulator API"
                testingAPI = component "Testing API"
                obstacleAPI = component "Obstacle API"
                mlAPI = component "Machine Learning API"
                featureExtractionAPI = component "Feature Extraction API"

                sklearn = component "sklearn"
                beamngpy = component "beamngpy"
                carla = component "carla"
            }
            beamngSimulator = container "BeamNG Simulator"
            carlaSimulator = container "CARLA Simulator"
        }


        user -> cli "uses"
        cli -> testingAPI "uses"
        cli -> mlAPI "uses"
        cli -> featureExtractionAPI "uses"
        testingAPI -> simulatorAPI "uses"
        testingAPI -> obstacleAPI "uses"
        mlAPI -> sklearn "uses"
        user -> sdcScissor "uses"
        python -> beamngSimulator "needs"
        python -> carlaSimulator "needs"
        simulatorAPI -> beamngpy "uses"
        simulatorAPI -> carla "uses"
        beamngpy -> beamngSimulator "controls"
        carla -> carlaSimulator "controls"
    }

    views {
        systemContext sdcScissor "Diagram1" {
            include *
            autoLayout
        }

        container sdcScissor "Diagram2" {
            include *
            autoLayout
        }

        component python "Diagram3" {
            include *
            autoLayout
        }

        theme default
    }
}
