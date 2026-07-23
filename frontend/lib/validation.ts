import { z } from 'zod'

export const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

export const userSchema = z.object({
  email: z.string().email(),
  nome: z.string().min(1),
  cognome: z.string().min(1),
  telefono: z.string().optional(),
  ruolo: z.enum(['admin', 'manager', 'user', 'guest']),
  stato: z.enum(['active', 'inactive', 'suspended']),
})

export const companySchema = z.object({
  ragione_sociale: z.string().min(1),
  partita_iva: z.string().min(11).max(16),
  tipo_cliente: z.enum(['enterprise', 'pme', 'freelance', 'other']),
  email: z.string().email(),
  telefono: z.string().optional(),
})

export const propertySchema = z.object({
  company: z.number(),
  indirizzo: z.string().min(1),
  comune: z.string().min(1),
  provincia: z.string().length(2),
  foglio: z.string().min(1),
  particella: z.string().min(1),
  subalterno: z.string().optional(),
  categoria_catastale: z.string().min(1),
  domus_score: z.number().min(0).max(100).optional(),
  status: z.enum(['active', 'inactive', 'archived']),
})
