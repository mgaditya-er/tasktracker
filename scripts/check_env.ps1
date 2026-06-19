Write-Host ""
Write-Host "Environment Validation"
Write-Host ""

python --version
git --version

Write-Host ""

try {
    docker --version
}
catch {
    Write-Host "Docker Not Installed"
}

try {
    kubectl version --client
}
catch {
    Write-Host "Kubectl Not Installed"
}

try {
    helm version
}
catch {
    Write-Host "Helm Not Installed"
}

try {
    terraform version
}
catch {
    Write-Host "Terraform Not Installed"
}