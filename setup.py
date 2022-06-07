from distutils.core import setup

setup(
    name="sdc-scissor",
    version="v2.0",
    packages=[
        "sdc_scissor",
        "sdc_scissor.testing_api",
        "sdc_scissor.testing_api.frenetic",
        "sdc_scissor.testing_api.frenetic.src",
        "sdc_scissor.testing_api.frenetic.src.utils",
        "sdc_scissor.testing_api.frenetic.src.generators",
        "sdc_scissor.simulator_api",
        "sdc_scissor.machine_learning_api",
        "sdc_scissor.feature_extraction_api",
        "self_driving",
    ],
    url="",
    license="GPLv3.0",
    author="Christian Birchler",
    author_email="birchler.chr@gmail.com",
    description="SDC-Scissor",
)
