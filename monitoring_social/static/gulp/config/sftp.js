
const ftpConfigGulp = import('../../../ftpLkFm.js').config;

const pathTemplate = '';

let deploy = false;
let resConfig = {host: ''};
if (ftpConfigGulp) {
  deploy = true;
  resConfig = ftpConfigGulp;
  resConfig.remotePath = resConfig.remotePath + pathTemplate;
}
export const isDeploy = deploy;
export const createPathForDeploy = (str) => {
  return {
    ...resConfig,
    remotePath: resConfig.remotePath + str,
  };
};
