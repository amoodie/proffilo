import numpy as np


def velocity_roughness_z0(d90):
    ks = 3 * d90
    z0 = ks
    return z0


def velocity_loglaw(z, z0, ustar, alpha=1):
    z[z<z0] = np.nan
    vel = (ustar / (alpha * 0.41)) * np.log(z / z0);
    return vel

# def concentration_rouse(z, flow_depth, b, cb, Rou):
#     # nEvalPts = 51;
#     modelEvalZs = np.linspace(flow_depth*0.05, flowDepth, nEvalPts)
#     modelEvalCs = cb .* ( ((flowDepth-modelEvalZs)./modelEvalZs) ./ Hbb ) .^ Rou
#     return modelEvalZs, modelEvalCs