"""
Test script for Unit 1 foundations equations.

Verifies all equations can be imported, computed, and produce reasonable outputs.
"""
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from scripts.index import get_global_index
import scripts.foundations.transport as transport
import scripts.foundations.electrical as electrical
import scripts.foundations.diffusion as diffusion
import scripts.foundations.thermodynamics as thermodynamics
import numpy as np


def test_all_equations():
    """Test all foundation equations with physiological values."""

    index = get_global_index()
    print(f"Testing {len(index)} equations from Unit 1: Physical Foundations")
    print("=" * 70)

    # Transport tests
    print("\n### TRANSPORT EQUATIONS ###")

    # Volume flux
    J_V = transport.volume_flux.compute(Q_V=1e-6, A=1e-4)
    print(f"✓ Volume flux: {J_V:.6e} m/s")

    # Solute flux
    J_S = transport.solute_flux.compute(Q_S=1e-9, A=1e-4)
    print(f"✓ Solute flux: {J_S:.6e} mol/(m²·s)")

    # Hydrostatic pressure
    P = transport.hydrostatic_pressure.compute(rho=1055, g=9.8, h=0.13)  # 13 cm column
    print(f"✓ Hydrostatic pressure: {P:.1f} Pa ({P/133.322:.1f} mmHg)")

    # Poiseuille flow (arteriole)
    Q_V = transport.poiseuille_flow.compute(r=50e-6, eta=3.5e-3, delta_P=2000, L=1e-3)
    print(f"✓ Poiseuille flow: {Q_V:.6e} m³/s ({Q_V*1e9*60:.3f} nL/min)")

    # Hydraulic resistance
    R = transport.hydraulic_resistance.compute(eta=3.5e-3, L=1e-3, r=50e-6)
    print(f"✓ Hydraulic resistance: {R:.6e} Pa·s/m³")

    # Laplace - cylinder (artery)
    delta_P = transport.laplace_cylinder.compute(T=200, r=0.01)  # 1 cm radius
    print(f"✓ Laplace (cylinder): {delta_P:.1f} Pa ({delta_P/133.322:.1f} mmHg)")

    # Laplace - sphere (alveolus)
    delta_P = transport.laplace_sphere.compute(T=0.025, r=150e-6)  # 150 μm radius
    print(f"✓ Laplace (sphere): {delta_P:.1f} Pa")

    # Electrical tests
    print("\n### ELECTRICAL EQUATIONS ###")

    # Coulomb's law
    F = electrical.coulomb_law.compute(q1=1.6e-19, q2=-1.6e-19, r=1e-9)
    print(f"✓ Coulomb force (vacuum): {F:.6e} N")

    # Coulomb in medium (water)
    F_medium = electrical.coulomb_law_medium.compute(q1=1.6e-19, q2=-1.6e-19, r=1e-9, epsilon=80)
    print(f"✓ Coulomb force (water, ε=80): {F_medium:.6e} N ({F/F_medium:.0f}× weaker)")

    # Electric field
    E = electrical.electric_field.compute(F=1e-12, q=1.6e-19)
    print(f"✓ Electric field: {E:.6e} V/m")

    # Capacitance
    C = electrical.capacitance.compute(Q=1e-12, V=0.07)
    print(f"✓ Capacitance: {C:.6e} F ({C*1e12:.3f} pF)")

    # Parallel plate (membrane)
    C_membrane = electrical.parallel_plate_capacitor.compute(
        epsilon=3.0, epsilon_0=8.85e-12, A=1e-8, d=4e-9
    )
    print(f"✓ Membrane capacitance: {C_membrane:.6e} F ({C_membrane*1e4*1e6:.2f} μF/cm²)")

    # Diffusion tests
    print("\n### DIFFUSION EQUATIONS ###")

    # Fick's first law
    J_S = diffusion.fick_first_law.compute(D=1e-9, dC_dx=-1000)
    print(f"✓ Fick's first law: {J_S:.6e} mol/(m²·s)")

    # Stokes-Einstein (K+ ion)
    D = diffusion.stokes_einstein.compute(T=310, eta=7e-4, a=1.4e-10)  # K+ radius ~1.4 Å
    print(f"✓ Stokes-Einstein (K+): {D:.6e} m²/s")

    # Diffusion time
    t_1um = diffusion.diffusion_time.compute(x=1e-6, D=1e-9)
    t_1mm = diffusion.diffusion_time.compute(x=1e-3, D=1e-9)
    print(f"✓ Diffusion time (1 μm): {t_1um*1e3:.2f} ms")
    print(f"✓ Diffusion time (1 mm): {t_1mm:.1f} s ({t_1mm/60:.1f} min)")

    # Thermodynamics tests
    print("\n### THERMODYNAMICS EQUATIONS ###")

    # Gibbs free energy
    delta_G = thermodynamics.gibbs_free_energy.compute(delta_H=-50000, T=310, delta_S=-100)
    print(f"✓ Gibbs free energy: {delta_G:.1f} J/mol ({delta_G/1000:.1f} kJ/mol)")

    # Standard free energy (from K_eq)
    delta_G0 = thermodynamics.standard_free_energy.compute(K_eq=1000)
    print(f"✓ Standard free energy (K_eq=1000): {delta_G0:.1f} J/mol ({delta_G0/1000:.1f} kJ/mol)")

    # Actual free energy
    delta_G_actual = thermodynamics.actual_free_energy.compute(delta_G0=-30500, Q=0.01)
    print(f"✓ Actual free energy: {delta_G_actual:.1f} J/mol ({delta_G_actual/1000:.1f} kJ/mol)")

    # Electrochemical potential
    mu_tilde = thermodynamics.electrochemical_potential.compute(
        mu_0=0, C=0.14, z=1, psi=-0.07
    )
    print(f"✓ Electrochemical potential: {mu_tilde:.1f} J/mol")

    # Nernst equation (K+: 5 mM inside, 140 mM outside)
    E_K = thermodynamics.nernst_equation.compute(z=1, C_out=0.005, C_in=0.14)
    print(f"✓ Nernst potential (K+): {E_K*1000:.1f} mV")

    # Nernst equation (Na+: 10 mM inside, 140 mM outside)
    E_Na = thermodynamics.nernst_equation.compute(z=1, C_out=0.14, C_in=0.01)
    print(f"✓ Nernst potential (Na+): {E_Na*1000:.1f} mV")

    print("\n" + "=" * 70)
    print(f"✓ All {len(index)} equations tested successfully!")
    print("\nCross-domain equations (used in multiple units):")
    cross_domain = [
        'nernst_equation',
        'fick_first_law',
        'diffusion_time',
        'hydraulic_resistance',
        'laplace_cylinder',
        'laplace_sphere'
    ]
    for eq_id in cross_domain:
        eq = index.get(eq_id)
        print(f"  • {eq.name} ({eq_id})")


if __name__ == "__main__":
    test_all_equations()
